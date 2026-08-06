# 🩺 MediVision AI — Intelligent Chest X-Ray Disease Detection System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?logo=tensorflow)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?logo=streamlit)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?logo=opencv)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

> **An AI-powered medical imaging application that automatically detects COVID-19, Viral Pneumonia, and Normal chest X-rays using Deep Transfer Learning, providing fast, accessible, and reliable preliminary screening assistance.**

---

# 📌 Overview

Chest X-ray interpretation is a time-consuming process that requires experienced radiologists, especially during high patient volumes. MediVision AI leverages **Transfer Learning with EfficientNetB0** to classify chest radiographs into:

- 🦠 COVID-19
- 🫁 Viral Pneumonia
- ✅ Normal

The project combines **Deep Learning**, **Computer Vision**, and a **modern Streamlit-based web application** to deliver an intuitive diagnostic assistant with real-time predictions, confidence scores, interactive visualizations, and downloadable medical reports.

---

# ✨ Key Features

- 🧠 Transfer Learning using EfficientNetB0
- 📊 Three-Class Chest X-Ray Classification
- ⚡ Real-Time AI Prediction
- 📈 Prediction Confidence Visualization
- 📄 Downloadable Professional PDF Reports
- 🖼️ Drag & Drop X-ray Upload
- 📱 Responsive Medical Dashboard
- 🎨 Modern Glassmorphism UI
- 🚀 Cached Model Loading for Faster Inference
- 🔍 Session-based Prediction History
- ⚠️ Medical Disclaimer Integration
- 🏥 Recruiter-Friendly Modular Architecture

---

# 📊 Model Performance

| Metric | Value |
|---------|-------|
| Model | EfficientNetB0 |
| Learning Strategy | Transfer Learning + Fine-Tuning |
| Classes | COVID, Normal, Viral Pneumonia |
| Input Size | 224 × 224 |
| Test Accuracy | **94.6%** |

---

# 🛠 Tech Stack

## Frontend

- Streamlit
- HTML/CSS
- Custom CSS (Glassmorphism UI)
- Plotly

---

## Backend

- Python
- TensorFlow / Keras
- NumPy
- OpenCV
- Pillow

---

## Machine Learning

- EfficientNetB0
- Transfer Learning
- Fine-Tuning
- TensorFlow Dataset API

---

## Data Processing

- OpenCV
- TensorFlow
- NumPy

---

## Visualization

- Plotly
- Matplotlib

---

## Report Generation

- ReportLab

---

## Development Tools

- Google Colab (Model Training)
- VS Code
- Git
- GitHub

---

# 📂 Project Structure

```text
COVID_XRAY_PROJECT/

├── app/
│   ├── streamlit_app.py
│   ├── styles.css
│   └── assets/
│
├── dataset/
│
├── models/
│   └── best_model.keras
│
├── notebooks/
│   ├── preprocessing.ipynb
│   ├── dataset_analysis.ipynb
│   ├── training.ipynb
│   ├── finetuning.ipynb
│   ├── evaluation.ipynb
│
├── reports/
│
├── utils/
│   ├── preprocessing.py
│   ├── predict.py
│   └── report_generator.py
│
├── requirements.txt
│
└── README.md
```

---

# 🏗 Project Architecture

```text
                 User Uploads Chest X-Ray
                          │
                          ▼
                 Image Preprocessing
                          │
                          ▼
               TensorFlow Prediction Pipeline
                          │
                          ▼
             EfficientNetB0 Deep Learning Model
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
     COVID            Normal       Viral Pneumonia
                          │
                          ▼
            Confidence & Probability Scores
                          │
                          ▼
             Interactive Streamlit Dashboard
                          │
                          ▼
          PDF Medical Report Generation
```

---

# ⚙️ System Workflow

```text
Upload Image
      │
      ▼
Image Validation
      │
      ▼
Resize → RGB Conversion → Tensor Conversion
      │
      ▼
EfficientNetB0 Prediction
      │
      ▼
Probability Calculation
      │
      ▼
Display Prediction
      │
      ▼
Generate PDF Report
```

---

# 🚧 Technical Challenges & Engineering Decisions

## 1. Building an Efficient Medical Imaging Model

**Challenge**

Training a high-performing medical image classifier on limited hardware.

**Solution**

- Leveraged **Transfer Learning** with EfficientNetB0 pretrained on ImageNet.
- Fine-tuned the backbone instead of training from scratch, significantly reducing training time while achieving **94.6% test accuracy**.

---

## 2. Optimizing Training for Limited Compute Resources

**Challenge**

Training deep CNNs on Google Colab Free Tier and a local laptop with limited compute.

**Solution**

- Used Google Colab T4 GPU for model training.
- Saved processed datasets to Google Drive to avoid repeated preprocessing.
- Implemented checkpointing and early stopping for efficient training.

---

## 3. Designing a Production-Ready AI Application

**Challenge**

Creating an interface that is intuitive for non-technical users while keeping inference fast.

**Solution**

- Built a modular Streamlit application.
- Cached the model using `st.cache_resource`.
- Separated preprocessing, prediction, and report generation into reusable utility modules.

---

# 🚀 Local Setup

## Prerequisites

- Python 3.10+
- Git
- pip

---

## Clone Repository

```bash
git clone https://github.com/HimakarPisipati/Medivision-AI.git

cd Medivision-AI
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Download Dataset (Important)

Due to file size constraints, the dataset is **not** included in this repository. 
1. Download the COVID-19 Radiography Dataset from Kaggle (or your specified source).
2. Extract the contents and place them inside the `dataset/` directory.

---

## Add Trained Model

Place your trained model inside:

```text
models/

best_model.keras
```

---

## Run Application

```bash
streamlit run app/streamlit_app.py
```

---

Application will be available at:

```text
http://localhost:8501
```

---

# 📸 Application Features

- AI-Powered Chest X-Ray Detection
- Drag & Drop Image Upload
- Real-Time Prediction
- Confidence Score
- Interactive Probability Chart
- Medical Information Panel
- Downloadable PDF Report
- Prediction History
- Responsive Modern UI

---

# 📈 Future Roadmap

- [ ] Grad-CAM Explainable AI Visualization
- [ ] Multi-Disease Chest X-Ray Detection
- [ ] DICOM File Support
- [ ] User Authentication
- [ ] Cloud Deployment (AWS / Azure / GCP)
- [ ] REST API with FastAPI
- [ ] Docker Containerization
- [ ] CI/CD Pipeline with GitHub Actions
- [ ] Model Monitoring Dashboard
- [ ] Mobile-Friendly Progressive Web App (PWA)

---

# 🎯 Key Learning Outcomes

Through this project, I gained hands-on experience in:

- Deep Learning for Medical Imaging
- Transfer Learning & Fine-Tuning
- Computer Vision with TensorFlow
- End-to-End ML Deployment
- Streamlit Application Development
- Modular Software Architecture
- Model Evaluation & Performance Analysis
- PDF Report Automation
- Git & Version Control

---

# ⚠️ Disclaimer

> **This project is intended for educational and research purposes only. It should not be used as a replacement for professional medical diagnosis or clinical decision-making.**

---

# 🔒 Data Privacy & Ethical Use

- **No Real Patient Data:** This system is trained on publicly available, anonymized academic datasets. Do not use this application to process or store real, un-anonymized patient data (PHI) to comply with HIPAA and data privacy laws.
- **Educational Scope:** The repository and its assets are provided strictly for resume-building, portfolio demonstration, and educational research.
- **No Commercial Medical Use:** The model is not FDA-approved or certified for clinical use and must not be used in a commercial medical environment.

---

# 👨‍💻 Author

**Himakar Pisipati**

B.Tech Computer Science & Engineering

Passionate about Artificial Intelligence, Computer Vision, Deep Learning, and Full-Stack AI Applications.

---

⭐ **If you found this project interesting, consider giving it a star!**