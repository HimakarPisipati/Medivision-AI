import cv2
import numpy as np
from PIL import Image

from tensorflow.keras.applications.resnet50 import preprocess_input

def preprocess_image(image_file):
    """
    Loads, resizes (224x224), converts to RGB, and normalizes the image.
    Returns a tensor suitable for ResNet50 prediction.
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
    
    # Add batch dimension
    img_tensor = np.expand_dims(img_resized, axis=0)
    
    # Apply ResNet50 preprocessing
    img_preprocessed = preprocess_input(img_tensor.astype(np.float32))
    
    return img_preprocessed
