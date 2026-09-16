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
from utils.gradcam import generate_gradcam

# Configure Page
st.set_page_config(
    page_title="MediVision AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme state initialization
if 'theme' not in st.session_state:
    st.session_state.theme = "Dark Mode"

# Load Base CSS
def load_css(css_file):
    try:
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        try:
            with open('styles.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except:
            pass

load_css('app/styles.css')

# Inject Light Mode CSS overrides if active
if st.session_state.theme == "Light Mode":
    st.markdown("""
    <style>
    :root {
        --bg-primary: #F8FAFC;
        --bg-secondary: #FFFFFF;
        --text-primary: #0F172A;
        --text-secondary: #475569;
        
        --card-bg: #FFFFFF;
        --card-border: rgba(0, 0, 0, 0.1);
        --card-shadow: rgba(0, 0, 0, 0.05);
        
        --metric-bg: #FFFFFF;
        
        --sidebar-bg: #F1F5F9;
        --sidebar-border: rgba(0, 0, 0, 0.1);
        
        --hover-bg: rgba(0, 0, 0, 0.05);
    }
    
    /* Ensure charts have dark text in light mode */
    .js-plotly-plot .plotly text {
        fill: #0F172A !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for history
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# Sidebar
with st.sidebar:
    # Custom Logo Block matching the screenshot
    st.markdown("""
    <div class='sidebar-logo-container'>
        <div class='sidebar-logo-icon'>🩻</div>
        <div class='sidebar-logo-text'>MediVision AI</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation items with icons
    pages = {
        "🎛️ Dashboard": "Dashboard",
        "🔍 Analyze X-Ray": "Analyze X-Ray",
        "🕒 Prediction History": "Prediction History",
        "🧠 Model Insights": "Model Insights",
        "ℹ️ About": "About"
    }
    
    selected_option = st.radio("", list(pages.keys()), label_visibility="collapsed")
    page = pages[selected_option]
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Theme Toggle Switch
    st.radio("🎨 Theme", ["Dark Mode", "Light Mode"], key="theme", horizontal=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='margin-bottom: 16px;'><span class='status-indicator'></span><span class='status-text'>Model Ready</span></div>", unsafe_allow_html=True)
    st.markdown("**Model:** EfficientNetB0<br>**Accuracy:** 94.6%", unsafe_allow_html=True)

# Load Model
model = load_cached_model()

# Helper Functions for UI components
def render_disclaimer():
    st.markdown("""
    <div class='medical-disclaimer'>
        <div class='disclaimer-title'>⚕ Educational & Research Use Only</div>
        <div class='disclaimer-text'>MediVision AI is intended for educational and research purposes. It is not a medical diagnostic tool and should not replace evaluation by a qualified healthcare professional.</div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div class='custom-footer'>
        MediVision AI • AI-Powered Chest X-Ray Analysis<br>
        Educational & Research Project • 2026<br>
    </div>
    """, unsafe_allow_html=True)


if page == "Dashboard":
    # Hero Section
    st.markdown("<div style='text-align: center; margin-top: 2rem; margin-bottom: 3rem;'>", unsafe_allow_html=True)
    st.markdown("<span class='badge'>AI-POWERED • EFFICIENTNETB0</span>", unsafe_allow_html=True)
    st.markdown("<h1>MediVision AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.25rem; color: var(--text-secondary); max-width: 600px; margin: 0 auto;'>Upload a chest X-ray and receive an AI-generated classification across COVID-19, Normal, and Viral Pneumonia.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Top metric cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Model Accuracy", "94.6%", "+2.1% tuning")
    col2.metric("Disease Classes", "3", "COVID, Normal, Pneumonia")
    col3.metric("Model Architecture", "EfficientNetB0")
    col4.metric("Image Resolution", "224 × 224")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("👈 Please select **Analyze X-Ray** from the sidebar to begin processing an image.")

elif page == "Analyze X-Ray":
    st.markdown("<h2>Analyze X-Ray</h2>", unsafe_allow_html=True)
    st.markdown("<p class='muted-text'>Upload a frontal chest X-ray image for AI inference.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    
    # Custom File Uploader UI hints
    st.markdown("""
    <div style='text-align: center; margin-bottom: 16px;'>
        <div style='font-size: 48px; margin-bottom: 8px;'>🩻</div>
        <h3 style='margin:0;'>Upload Chest X-Ray</h3>
        <p class='helper-text'>Supported formats: PNG, JPG, JPEG<br>Maximum recommended image quality: High-resolution frontal chest X-ray</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_file is not None:
        if model is None:
            st.error("Model could not be loaded. Please ensure 'models/best_model.keras' exists.")
        else:
            col_img, col_results = st.columns([1, 1.5])
            
            with col_img:
                st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                st.markdown("<h3>Uploaded Image</h3>", unsafe_allow_html=True)
                img = Image.open(uploaded_file)
                st.image(img, use_container_width=True)
                
                # Image metadata
                st.markdown(f"""
                <div class='info-grid' style='margin-top: 16px;'>
                    <div class='info-card'>
                        <div class='info-label'>Filename</div>
                        <div class='info-val' style='font-size: 14px; word-break: break-all;'>{uploaded_file.name}</div>
                    </div>
                    <div class='info-card'>
                        <div class='info-label'>Dimensions</div>
                        <div class='info-val'>{img.size[0]} × {img.size[1]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col_results:
                # Preprocess and Predict
                with st.spinner("Analyzing image..."):
                    try:
                        uploaded_file.seek(0)
                        img_tensor = preprocess_image(uploaded_file)
                        predicted_class, confidence, probabilities, inference_time = predict_disease(model, img_tensor)
                        error_occurred = False
                    except Exception as e:
                        st.error("Unable to process this image. Please upload a valid PNG, JPG, or JPEG chest X-ray.")
                        error_occurred = True
                
                if not error_occurred:
                    # Result Card
                    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                    st.markdown("<div class='prediction-title'>Model Prediction</div>", unsafe_allow_html=True)
                    
                    # Color semantics
                    css_class = "color-normal"
                    bg_class = "bg-normal"
                    if predicted_class == "COVID":
                        css_class = "color-covid"
                        bg_class = "bg-covid"
                    elif predicted_class == "Viral Pneumonia":
                        css_class = "color-pneumonia"
                        bg_class = "bg-pneumonia"
                        
                    st.markdown(f"<div class='prediction-result {css_class}'>{predicted_class}</div>", unsafe_allow_html=True)
                    
                    # Confidence visualization
                    conf_text = "High Confidence" if confidence > 85 else ("Medium Confidence" if confidence > 60 else "Low Confidence")
                    st.markdown(f"""
                    <div>
                        <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                            <span style='font-weight: 600;'>Confidence: {confidence:.2f}%</span>
                            <span class='muted-text' style='font-size: 14px;'>{conf_text}</span>
                        </div>
                        <div class='confidence-container'>
                            <div class='confidence-fill {bg_class}' style='width: {confidence}%;'></div>
                        </div>
                        <div class='helper-text' style='margin-top: 8px;'>This score represents the model's confidence in its predicted class.</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Low confidence warning
                    if confidence < 70:
                        st.warning("⚠ **Low Confidence Prediction:** The model is uncertain about this result. Consider reviewing the image quality or using a clinically appropriate X-ray.")
                        
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Probabilities & Details Card
                    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                    st.markdown("<h3>Class Probabilities</h3>", unsafe_allow_html=True)
                    
                    # Plotly Chart
                    classes = ['COVID', 'Normal', 'Viral Pneumonia']
                    df = pd.DataFrame({
                        'Class': classes,
                        'Probability': [p * 100 for p in probabilities]
                    })
                    
                    # Determine text color based on theme
                    text_col = '#0F172A' if st.session_state.theme == "Light Mode" else '#F8FAFC'
                    
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
                        font_color=text_col,
                        margin=dict(l=0, r=0, t=0, b=0),
                        height=150,
                        xaxis=dict(range=[0, 100], showgrid=False, title=""),
                        yaxis=dict(showgrid=False, title=""),
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Info Grid
                    st.markdown(f"""
                    <div class='info-grid'>
                        <div class='info-card'>
                            <div class='info-label'>Inference Time</div>
                            <div class='info-val'>{(inference_time*1000):.1f} ms</div>
                        </div>
                        <div class='info-card'>
                            <div class='info-label'>Model</div>
                            <div class='info-val'>EfficientNetB0</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # PDF Download
                    uploaded_file.seek(0)
                    pdf_bytes = generate_pdf_report(uploaded_file, predicted_class, confidence, probabilities, inference_time)
                    
                    st.download_button(
                        label="↓ Download Analysis Report",
                        data=pdf_bytes,
                        file_name=f"MediVision_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    # Save to history
                    if not any(item['filename'] == uploaded_file.name for item in st.session_state.prediction_history):
                        uploaded_file.seek(0)
                        st.session_state.prediction_history.append({
                            'filename': uploaded_file.name,
                            'prediction': predicted_class,
                            'confidence': confidence,
                            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
            
            if not error_occurred:
                # Grad-CAM Visual Explainability Section
                st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                st.markdown("<h3 style='margin-top: 0;'>Model Attention Analysis (Grad-CAM)</h3>", unsafe_allow_html=True)
                st.markdown("""
                <p class='helper-text' style='margin-bottom: 20px;'>
                    Grad-CAM highlights image regions that contributed to the model's prediction. 
                    It is provided for model interpretability and educational purposes and should 
                    not be considered a medical diagnostic explanation.
                </p>
                """, unsafe_allow_html=True)
                
                try:
                    predicted_index = classes.index(predicted_class)
                    with st.spinner("Generating attention heatmap..."):
                        heatmap_rgb, overlay = generate_gradcam(model, img_tensor, predicted_index, original_image=img)
                    
                    cam_col1, cam_col2, cam_col3 = st.columns(3)
                    with cam_col1:
                        st.markdown("<div class='cam-col-header'>Original X-Ray</div>", unsafe_allow_html=True)
                        st.image(img, use_container_width=True)
                    with cam_col2:
                        st.markdown("<div class='cam-col-header'>Grad-CAM Heatmap</div>", unsafe_allow_html=True)
                        st.image(heatmap_rgb, use_container_width=True)
                    with cam_col3:
                        st.markdown("<div class='cam-col-header'>Attention Overlay</div>", unsafe_allow_html=True)
                        st.image(overlay, use_container_width=True)
                except Exception as e:
                    import logging
                    logging.getLogger(__name__).error(f"Grad-CAM generation failed: {e}", exc_info=True)
                    st.warning("⚠ **Grad-CAM visualization is temporarily unavailable.** The prediction result is still available.")
                
                st.markdown("</div>", unsafe_allow_html=True)

    
    render_disclaimer()

elif page == "Prediction History":
    st.markdown("<h2>Prediction History</h2>", unsafe_allow_html=True)
    st.markdown("<p class='muted-text'>Recent X-ray analyses performed during this session.</p>", unsafe_allow_html=True)
    
    if not st.session_state.prediction_history:
        st.info("No predictions made in this session yet. Go to **Analyze X-Ray** to begin.")
    else:
        for idx, item in enumerate(reversed(st.session_state.prediction_history)):
            st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            with col1:
                st.markdown("<div class='info-label'>File</div>", unsafe_allow_html=True)
                st.markdown(f"**{item['filename']}**")
            with col2:
                st.markdown("<div class='info-label'>Prediction</div>", unsafe_allow_html=True)
                
                # Semantic coloring for text
                color = "var(--color-normal)"
                if item['prediction'] == "COVID":
                    color = "var(--color-covid)"
                elif item['prediction'] == "Viral Pneumonia":
                    color = "var(--color-pneumonia)"
                    
                st.markdown(f"<strong style='color:{color}'>{item['prediction']}</strong>", unsafe_allow_html=True)
            with col3:
                st.markdown("<div class='info-label'>Confidence</div>", unsafe_allow_html=True)
                st.markdown(f"**{item['confidence']:.2f}%**")
            with col4:
                st.markdown("<div class='info-label'>Time</div>", unsafe_allow_html=True)
                st.markdown(f"{item['time']}")
            st.markdown("</div>", unsafe_allow_html=True)

elif page == "Model Insights":
    st.markdown("<h2>Model Insights</h2>", unsafe_allow_html=True)
    st.markdown("<p class='muted-text'>Technical details and performance metrics of the underlying AI model.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Architecture</h3>", unsafe_allow_html=True)
        st.markdown("""
        **EfficientNetB0** was chosen for its optimal balance of accuracy and computational efficiency.
        - **Transfer Learning:** Pre-trained on ImageNet.
        - **Fine-Tuning:** Tailored for chest X-ray classification.
        - **Parameters:** ~5.3 million.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Performance</h3>", unsafe_allow_html=True)
        st.markdown("""
        - **Test Accuracy:** 94.6%
        - **Input Resolution:** 224 × 224 pixels
        - **Output Classes:** 3 (COVID, Normal, Viral Pneumonia)
        - **Average Inference Time:** < 50ms (CPU)
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h3>Inference Pipeline</h3>", unsafe_allow_html=True)
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    
    # Adjust background inline based on theme for the pipeline
    bg_color = "rgba(0,0,0,0.05)" if st.session_state.theme == "Light Mode" else "rgba(255,255,255,0.02)"
    
    # Pipeline visualization via HTML
    st.markdown(f"""
    <div style='display: flex; flex-direction: column; gap: 16px;'>
        <div style='display: flex; align-items: center; gap: 16px; background: {bg_color}; padding: 16px; border-radius: 8px;'>
            <div style='font-size: 24px;'>🖼️</div>
            <div><strong>1. Input:</strong> Raw Chest X-Ray Image</div>
        </div>
        <div style='display: flex; align-items: center; gap: 16px; background: {bg_color}; padding: 16px; border-radius: 8px;'>
            <div style='font-size: 24px;'>⚙️</div>
            <div><strong>2. Preprocessing:</strong> Resize to 224x224, Normalize pixel values</div>
        </div>
        <div style='display: flex; align-items: center; gap: 16px; background: rgba(37,99,235,0.1); padding: 16px; border-radius: 8px; border: 1px solid rgba(37,99,235,0.3);'>
            <div style='font-size: 24px;'>🧠</div>
            <div><strong>3. Inference:</strong> EfficientNetB0 Feature Extraction & Classification</div>
        </div>
        <div style='display: flex; align-items: center; gap: 16px; background: {bg_color}; padding: 16px; border-radius: 8px;'>
            <div style='font-size: 24px;'>📊</div>
            <div><strong>4. Output:</strong> Class probabilities and final prediction</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "About":
    st.markdown("<h2>About MediVision AI</h2>", unsafe_allow_html=True)
    st.markdown("<p class='muted-text'>Empowering medical research with Artificial Intelligence.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("<h3>What is MediVision AI?</h3>", unsafe_allow_html=True)
    st.write("MediVision AI is a state-of-the-art deep learning application designed to assist in the rapid classification of chest X-rays into three categories: COVID, Normal, and Viral Pneumonia. It demonstrates the potential of computer vision in assisting healthcare professionals.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("<h3>How It Works</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='pipeline-step'>
        <div class='step-number'>01</div>
        <div class='step-content'>
            <h4>Upload</h4>
            <p>Upload a standard frontal chest X-ray image (PNG or JPG).</p>
        </div>
    </div>
    <div class='pipeline-step'>
        <div class='step-number'>02</div>
        <div class='step-content'>
            <h4>Process</h4>
            <p>The image is automatically resized and normalized for the AI model.</p>
        </div>
    </div>
    <div class='pipeline-step'>
        <div class='step-number'>03</div>
        <div class='step-content'>
            <h4>Analyze</h4>
            <p>Our fine-tuned EfficientNetB0 model extracts features and computes probabilities.</p>
        </div>
    </div>
    <div class='pipeline-step'>
        <div class='step-number'>04</div>
        <div class='step-content'>
            <h4>Predict</h4>
            <p>The system returns the most likely class with a confidence score.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='premium-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h3>Technology Stack</h3>", unsafe_allow_html=True)
        st.write("- **Frontend:** Streamlit with custom Glassmorphism UI")
        st.write("- **Backend/Modeling:** TensorFlow, Keras")
        st.write("- **Image Processing:** OpenCV, Pillow, NumPy")
        st.write("- **Visualization:** Plotly")
        st.write("- **Reporting:** ReportLab")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='premium-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h3>Limitations</h3>", unsafe_allow_html=True)
        st.write("- Not trained on pediatric X-rays.")
        st.write("- May struggle with poor quality or highly obscured images.")
        st.write("- Only detects 3 specific classes; ignores other lung conditions.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    render_disclaimer()

if page != "Dashboard":
    render_footer()
