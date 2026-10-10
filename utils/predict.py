import time
import numpy as np
import streamlit as st
import tensorflow as tf

# Define classes as requested
CLASSES = ['COVID', 'Normal', 'Viral Pneumonia']

MODEL_PATH = 'models/ResNet50_final.keras'

@st.cache_resource
def load_cached_model():
    """
    Loads the cached ResNet50 model.
    """
    import os
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model file not found at {MODEL_PATH}. Please copy your trained model from Google Drive (MyDrive/computervisionproject/model_comparison/ResNet50/ResNet50_final.keras) into the local 'models/' directory.")
        return None
    try:
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def predict_disease(model, image_tensor):
    """
    Predicts the disease from the image tensor.
    Returns predicted class, confidence, probabilities, and inference time.
    """
    start_time = time.time()
    
    # Predict
    predictions = model.predict(image_tensor)
    
    # Inference time
    inference_time = time.time() - start_time
    
    # Calculate probabilities and confidence
    probabilities = predictions[0]
    
    # Note: Depending on whether the model outputs logits or softmax, 
    # we might need to apply softmax. Assuming the model outputs softmax probabilities.
    # If the sum is not close to 1, we apply softmax.
    if not np.isclose(np.sum(probabilities), 1.0, atol=0.1):
        probabilities = tf.nn.softmax(probabilities).numpy()
        
    predicted_index = np.argmax(probabilities)
    predicted_class = CLASSES[predicted_index]
    confidence = probabilities[predicted_index] * 100
    
    return predicted_class, confidence, probabilities, inference_time
