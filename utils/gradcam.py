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
        
        # Access nested model layers
        efficientnet = model.get_layer("efficientnetb0")
        gap = model.get_layer("global_average_pooling2d")
        dropout = model.get_layer("dropout")
        dense = model.get_layer("dense")
        
        # Access sequential augmentation layer if present
        try:
            preprocessing_layer = model.get_layer("sequential")
        except Exception:
            preprocessing_layer = None
            
        # Record operations with GradientTape
        with tf.GradientTape() as tape:
            if preprocessing_layer is not None:
                processed_image = preprocessing_layer(input_tensor, training=False)
            else:
                processed_image = input_tensor
                
            features = efficientnet(processed_image, training=False)
            pooled = gap(features)
            dropped = dropout(pooled, training=False)
            predictions = dense(dropped)
            class_score = predictions[:, predicted_index]
            
        # Compute gradients of class score with respect to feature maps
        gradients = tape.gradient(class_score, features)
        if gradients is None:
            raise ValueError("Gradients could not be computed for the specified layer and class.")
            
        # Global average pooling of gradients (channel-wise weights)
        pooled_gradients = tf.reduce_mean(gradients, axis=(1, 2))
        
        # Remove batch dimension
        features_single = features[0]
        pooled_gradients_single = pooled_gradients[0]
        
        # Compute weighted sum of feature maps
        heatmap = tf.reduce_sum(features_single * pooled_gradients_single, axis=-1)
        
        # Apply ReLU to keep only features that have a positive influence
        heatmap = tf.maximum(heatmap, 0)
        
        # Normalize heatmap between 0 and 1
        max_val = tf.reduce_max(heatmap)
        heatmap = heatmap / (max_val + 1e-8)
        heatmap = heatmap.numpy()
        
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
