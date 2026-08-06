import cv2
import numpy as np
from PIL import Image

def preprocess_image(image_file):
    """
    Loads, resizes (224x224), converts to RGB, and normalizes the image.
    Returns a tensor suitable for EfficientNetB0 prediction.
    """
    # Read the image file using PIL
    img = Image.open(image_file)
    
    # Convert to RGB (in case of grayscale or RGBA)
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    # Convert to numpy array
    img_array = np.array(img)
    
    # Resize to 224x224
    img_resized = cv2.resize(img_array, (224, 224))
    
    # Normalize if needed (EfficientNetB0 usually expects [0, 255], 
    # but some fine-tuned versions expect [0, 1]. We'll keep [0, 255] as default for Keras EfficientNet, 
    # but adding an expand_dims to make it a batch of 1).
    img_tensor = np.expand_dims(img_resized, axis=0)
    
    return img_tensor
