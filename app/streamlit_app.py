import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image

# Add project root to path for utils import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.preprocessing import preprocess_image
from utils.predict import load_cached_model, predict_disease
from utils.report_generator import generate_pdf_report

# Configure Page
st.set_page_config(
    page_title="MediVision AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css('app/styles.css')
except FileNotFoundError:
    try:
        load_css('styles.css') # If run from inside app folder
    except:
        pass

# Initialize session state for history
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# Sidebar
with st.sidebar:
    st.markdown("## MediVision AI 🧬")
    st.markdown("---")
    page = st.radio("Navigation", ["Dashboard", "Prediction History", "About"])
    
    if page == "Dashboard":
        st.markdown("---")
        st.markdown("### Model Information")
        st.info("**Name**: EfficientNetB0\n\n**Type**: Transfer Learning\n\n**Input**: 224x224 RGB\n\n**Classes**: 3\n\n**Accuracy**: 94.6%")

# Load Model
model = load_cached_model()

if page == "Dashboard":
    # Hero Section
    st.markdown("<h1 style='text-align: center;'>MediVision AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #94A3B8;'>AI-Powered Chest X-Ray Disease Detection</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upload Section in a card
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Chest X-Ray", type=["png", "jpg", "jpeg"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_file is not None:
        if model is None:
            st.error("Model could not be loaded. Please ensure 'models/best_model.keras' exists.")
        else:
            # Layout for results
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### Uploaded Image")
                img = Image.open(uploaded_file)
                st.image(img, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col2:
                # Preprocess and Predict
                with st.spinner("Analyzing image..."):
                    img_tensor = preprocess_image(uploaded_file)
                    predicted_class, confidence, probabilities, inference_time = predict_disease(model, img_tensor)
                
                # Result Card
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("<div class='prediction-title'>Diagnosis Prediction</div>", unsafe_allow_html=True)
                
                # Color code based on class
                color = "#38BDF8"
                if predicted_class == "COVID":
                    color = "#EF4444" # Red for covid
                elif predicted_class == "Viral Pneumonia":
                    color = "#F59E0B" # Orange for pneumonia
                else:
                    color = "#10B981" # Green for normal
                    
                st.markdown(f"<p class='confidence-value' style='color: {color};'>{predicted_class}</p>", unsafe_allow_html=True)
                st.markdown(f"**Confidence:** {confidence:.2f}% | **Inference Time:** {inference_time:.3f}s", unsafe_allow_html=True)
                
                # Recommendations based on prediction
                st.markdown("#### Recommendation")
                if predicted_class == "COVID":
                    st.warning("High probability of COVID-19 detected. Immediate isolation and RT-PCR test recommended. Consult a healthcare professional immediately.")
                elif predicted_class == "Viral Pneumonia":
                    st.warning("Signs of Viral Pneumonia detected. Please consult a pulmonologist for further clinical evaluation.")
                else:
                    st.success("No signs of COVID-19 or Viral Pneumonia detected. However, if symptoms persist, consult a doctor.")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Probability Visualization Card
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### Class Probabilities")
                
                # Plotly Chart
                classes = ['COVID', 'Normal', 'Viral Pneumonia']
                df = pd.DataFrame({
                    'Class': classes,
                    'Probability': [p * 100 for p in probabilities]
                })
                
                fig = px.bar(
                    df, 
                    x='Probability', 
                    y='Class', 
                    orientation='h',
                    color='Class',
                    color_discrete_map={
                        'COVID': '#EF4444',
                        'Normal': '#10B981',
                        'Viral Pneumonia': '#F59E0B'
                    }
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#F8FAFC',
                    margin=dict(l=0, r=0, t=0, b=0),
                    height=200,
                    xaxis=dict(range=[0, 100], showgrid=False),
                    yaxis=dict(showgrid=False),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # PDF Report Button
                # Need to rewind file pointer for reportlab
                uploaded_file.seek(0)
                pdf_bytes = generate_pdf_report(uploaded_file, predicted_class, confidence, probabilities, inference_time)
                
                st.download_button(
                    label="📄 Download Patient Report (PDF)",
                    data=pdf_bytes,
                    file_name=f"MediVision_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                # Save to history
                if not any(item['filename'] == uploaded_file.name for item in st.session_state.prediction_history):
                    st.session_state.prediction_history.append({
                        'filename': uploaded_file.name,
                        'prediction': predicted_class,
                        'confidence': confidence,
                        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

    # Disclaimer
    st.markdown("<div class='disclaimer'>This AI prediction is intended only for educational and research purposes. It should not replace professional medical diagnosis.</div>", unsafe_allow_html=True)

elif page == "Prediction History":
    st.markdown("## Prediction History")
    st.markdown("Session-based history of analyzed X-rays.")
    
    if not st.session_state.prediction_history:
        st.info("No predictions made in this session yet.")
    else:
        for idx, item in enumerate(reversed(st.session_state.prediction_history)):
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(f"**File:** {item['filename']}")
            col2.markdown(f"**Prediction:** {item['prediction']}")
            col3.markdown(f"**Confidence:** {item['confidence']:.2f}%")
            col4.markdown(f"**Time:** {item['time']}")
            st.markdown("</div>", unsafe_allow_html=True)

elif page == "About":
    st.markdown("## About MediVision AI")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### Overview")
    st.write("MediVision AI is a state-of-the-art deep learning application designed to assist in the rapid classification of chest X-rays into three categories: COVID, Normal, and Viral Pneumonia.")
    
    st.markdown("### Technology Stack")
    st.write("- **Frontend**: Streamlit with custom CSS (Glassmorphism design)")
    st.write("- **Backend/Modeling**: TensorFlow, Keras (EfficientNetB0)")
    st.write("- **Image Processing**: OpenCV, Pillow, NumPy")
    st.write("- **Visualization**: Plotly")
    st.write("- **Reporting**: ReportLab")
    
    st.markdown("### Model Architecture & Training")
    st.write("The core of this application is powered by **EfficientNetB0**, a highly efficient convolutional neural network. The model was trained using **Transfer Learning** on a large dataset of chest X-rays. After initial feature extraction, the model underwent **Fine-Tuning** to adapt to the specific nuances of COVID-19 and pneumonia indicators.")
    
    st.markdown("#### Evaluation Metrics")
    st.write("- **Accuracy**: 94.6%")
    st.write("- **Input Size**: 224x224 RGB")
    st.write("- **Classes**: COVID, Normal, Viral Pneumonia")
    
    st.markdown("</div>", unsafe_allow_html=True)

