import logging
import cv2
import numpy as np
import tensorflow as tf

logger = logging.getLogger(__name__)

def generate_gradcam(model, input_image, predicted_index, original_image=None):
    """
    Generates a Grad-CAM heatmap and blended overlay for a given model and input image.
    
    Parameters:
        model (tf.keras.Model): Trained MediVision AI classification model (EfficientNetB0-based).
        input_image (np.ndarray or tf.Tensor): Preprocessed input image tensor of shape (1, 224, 224, 3)
                                              or (224, 224, 3).
        predicted_index (int): Index of the target class for Grad-CAM explanation.
        original_image (PIL.Image or np.ndarray, optional): The original image before preprocessing.
                                                            Used as the base for resolution-matched overlay.
                                                            If None, input_image is used as base.
                                                            
    Returns:
        tuple: (heatmap_rgb, overlay)
            - heatmap_rgb (np.ndarray): Colorized JET heatmap in RGB format, uint8.
            - overlay (np.ndarray): Blended image (65% original + 35% heatmap) in RGB format, uint8.
    """
    try:
        # Ensure batch dimension
        if len(input_image.shape) == 3:
            input_image = np.expand_dims(input_image, axis=0)
            
        input_tensor = tf.cast(input_image, tf.float32)
        
        # Identify the last convolutional layer dynamically
        nested_model = None
        last_conv_layer_name = None
        
        def get_layer_shape(layer):
            try:
                if hasattr(layer, 'output_shape') and layer.output_shape is not None:
                    if isinstance(layer.output_shape, list): return layer.output_shape[0]
                    return layer.output_shape
                if hasattr(layer, 'output') and hasattr(layer.output, 'shape'):
                    return layer.output.shape
            except Exception:
                pass
            return None

        # Check if the backbone is nested
        for layer in model.layers:
            if isinstance(layer, tf.keras.Model):
                nested_model = layer
                break
                
        if nested_model:
            for layer in reversed(nested_model.layers):
                shape = get_layer_shape(layer)
                if shape is not None and len(shape) == 4:
                    last_conv_layer_name = layer.name
                    break
            if not last_conv_layer_name:
                raise ValueError("Could not find a convolutional layer in the nested model.")
                
            last_conv_layer = nested_model.get_layer(last_conv_layer_name)
            inner_grad_model = tf.keras.Model(nested_model.inputs, [last_conv_layer.output, nested_model.output])
            
            with tf.GradientTape() as tape:
                # Forward pass up to the nested model
                x = input_tensor
                for layer in model.layers:
                    if layer == nested_model:
                        break
                    if not isinstance(layer, tf.keras.layers.InputLayer):
                        x = layer(x)
                    
                conv_outputs, nested_out = inner_grad_model(x)
                tape.watch(conv_outputs)
                
                # Forward pass for the rest of the model
                x_out = nested_out
                past_nested = False
                for layer in model.layers:
                    if past_nested:
                        if not isinstance(layer, tf.keras.layers.InputLayer):
                            x_out = layer(x_out)
                    if layer == nested_model:
                        past_nested = True
                
                preds = x_out
                class_score = preds[:, predicted_index]
                
        else:
            # Flat model
            for layer in reversed(model.layers):
                shape = get_layer_shape(layer)
                if shape is not None and len(shape) == 4:
                    last_conv_layer_name = layer.name
                    break
                    
            if not last_conv_layer_name:
                raise ValueError("Could not find a convolutional layer in the model.")
                
            last_conv_layer = model.get_layer(last_conv_layer_name)
            grad_model = tf.keras.Model(model.inputs, [last_conv_layer.output, model.output])
            
            with tf.GradientTape() as tape:
                conv_outputs, preds = grad_model(input_tensor)
                tape.watch(conv_outputs)
                class_score = preds[:, predicted_index]
                
        # Compute gradients
        gradients = tape.gradient(class_score, conv_outputs)
        if gradients is None:
            raise ValueError("Gradients could not be computed for the selected layer.")
            
        # Global average pooling of gradients
        pooled_gradients = tf.reduce_mean(gradients, axis=(0, 1, 2))
        
        # Remove batch dimension from features
        features_single = conv_outputs[0]
        
        # Compute weighted sum
        heatmap = tf.reduce_sum(features_single * pooled_gradients, axis=-1)
        
        # Apply ReLU to keep only features that have a positive influence
        heatmap = tf.maximum(heatmap, 0)
        
        # Normalize heatmap between 0 and 1
        max_val = tf.reduce_max(heatmap)
        heatmap = heatmap / (max_val + 1e-8)
        heatmap = heatmap.numpy().astype('float32')
        
        # Prepare the base image for display and overlay
        if original_image is not None:
            if hasattr(original_image, 'convert'):
                base_img = np.array(original_image.convert('RGB'))
            else:
                base_img = np.array(original_image)
                if base_img.ndim == 2:
                    base_img = cv2.cvtColor(base_img, cv2.COLOR_GRAY2RGB)
                elif base_img.shape[-1] == 4:
                    base_img = cv2.cvtColor(base_img, cv2.COLOR_RGBA2RGB)
                    
            if base_img.dtype != np.uint8:
                if base_img.max() <= 1.0:
                    base_img = np.uint8(base_img * 255)
                else:
                    base_img = np.uint8(base_img)
        else:
            squeezed = np.squeeze(input_image)
            if squeezed.max() <= 1.0:
                base_img = np.uint8(squeezed * 255)
            else:
                base_img = np.uint8(squeezed)
                
        target_h, target_w = base_img.shape[0], base_img.shape[1]
        
        # Resize heatmap to match base image dimensions
        heatmap_resized = cv2.resize(heatmap, (target_w, target_h))
        
        # Apply JET colormap and convert to RGB
        heatmap_color = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
        heatmap_rgb = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)
        
        # Blend original image with heatmap (0.65 original + 0.35 heatmap)
        overlay = cv2.addWeighted(base_img, 0.65, heatmap_rgb, 0.35, 0)
        
        return heatmap_rgb, overlay
        
    except Exception as e:
        logger.error(f"Error generating Grad-CAM: {e}", exc_info=True)
        raise e
