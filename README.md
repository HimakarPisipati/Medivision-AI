# 🩺 MediVision AI — Intelligent Chest X-Ray Disease Detection System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?logo=tensorflow)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?logo=opencv)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

> **An AI-powered medical imaging application that automatically detects COVID-19, Viral Pneumonia, and Normal chest X-rays using Deep Transfer Learning, providing fast, accessible, and reliable preliminary screening assistance.**

---

# 📌 Overview

Chest X-ray interpretation is a time-consuming process that requires experienced radiologists, especially during high patient volumes. MediVision AI leverages **Transfer Learning with ResNet50** to classify chest radiographs into:

- 🦠 COVID-19
- 🫁 Viral Pneumonia
- ✅ Normal

The project combines **Deep Learning**, **Computer Vision**, a high-performance **FastAPI asynchronous backend**, and a modern **React + TypeScript frontend** to deliver an intuitive diagnostic assistant with real-time predictions, confidence scores, Grad-CAM visual explainability, and downloadable medical PDF reports.

---

# ✨ Key Features

- 🧠 Transfer Learning using ResNet50 (Fine-Tuned)
- 📊 Three-Class Chest X-Ray Classification (COVID, Normal, Viral Pneumonia)
- ⚡ Real-Time AI Inference via FastAPI Asynchronous REST API
- 🔍 Grad-CAM Explainable AI Heatmaps & Visual Overlays
- 📈 Prediction Confidence Visualization & Comparative Benchmarks
- 📄 Downloadable Clinical PDF Reports with Embedded Heatmaps
- 🖼️ Drag & Drop X-ray Upload with Real-Time Validation
- 📱 Responsive Medical Dashboard built with React & Tailwind CSS
- 🎨 Premium Clinical UI with Interactive Modals & Visual Analytics
- 🚀 Cached Model Loading Singleton Pattern for Sub-Second Inference
- 🔍 Session-based Diagnostic History
- ⚠️ Clinical Disclaimer & Confidence Caution Thresholds

---

# 📊 Model Performance

| Metric | Value |
|---------|-------|
| Model Architecture | ResNet50 (Transfer Learning + Stage 2 Fine-Tuning) |
| Classes | COVID, Normal, Viral Pneumonia |
| Input Resolution | 224 × 224 × 3 |
| Test Accuracy | **98.09%** |
| Weighted Precision | **98.10%** |
| Weighted Recall | **98.09%** |
| Weighted F1-Score | **98.08%** |
| ROC-AUC | **0.9980** |

---

# 🛠 Tech Stack

## Frontend

- Lovable.dev (AI Frontend Generation & Prototyping)
- React 18 / Vite
- TypeScript
- Tailwind CSS / Radix UI
- Lucide React
- Recharts (Interactive Clinical Charts)

---

## Backend

- FastAPI
- Uvicorn (ASGI Production Server)
- Python 3.11+
- TensorFlow / Keras (ResNet50)
- NumPy / Pandas
- OpenCV / Pillow
- ReportLab (Clinical PDF Engine)

---

## Machine Learning

- ResNet50
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

- Lovable.dev (AI-Assisted Frontend Development)
- Google Colab (Model Training)
- VS Code
- Git
- GitHub

---

# 📂 Project Structure

```text
COVID_XRAY_PROJECT/

├── app/
│   └── main.py                     # FastAPI REST API Application
│
├── frontend/                       # React 18 + TypeScript + Vite UI
│   ├── src/
│   │   ├── components/             # Reusable UI components
│   │   ├── pages/                  # Dashboard, Analysis, Insights, History
│   │   ├── services/               # API clients (predict, health, evaluation)
│   │   └── types/                  # TypeScript interface contracts
│   ├── package.json
│   └── vite.config.ts
│
├── dataset/
│
├── models/
│   └── ResNet50_final.keras        # Trained weights
│
├── notebooks/
│   ├── 01_preprocessing.ipynb
│   ├── 02_dataset_analysis.ipynb
│   ├── 03_training_ResNet50.ipynb
│   ├── 04_fine_tuning.ipynb
│   └── 05_evaluation.ipynb
│
├── model_comparison/
│   └── model_comparison_summary.csv
│
├── reports/
│   ├── classification_report.txt
│   ├── confusion_matrix.png
│   └── dataset_statistics.csv
│
├── utils/
│   ├── preprocessing.py            # Image preprocessing pipeline
│   ├── predict.py                  # Singleton inference engine
│   ├── gradcam.py                  # Grad-CAM explainability generator
│   └── report_generator.py         # ReportLab PDF report generator
│
├── requirements.txt
└── README.md
```

---

# 🏗 Project Architecture

```text
                  User Uploads Chest X-Ray
                           │
                           ▼
                 React + TypeScript Frontend
                           │
                           ▼ (Multipart REST API /api/predict)
                 FastAPI Asynchronous Backend
                           │
                           ▼
                  Image Preprocessing
                           │
                           ▼
                TensorFlow Prediction Pipeline
                           │
                           ▼
              ResNet50 Deep Learning Model
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
      COVID            Normal       Viral Pneumonia
                           │
                           ▼
             Confidence & Probability Scores
                           │
         ┌─────────────────┴─────────────────┐
         ▼                                   ▼
 Grad-CAM Heatmap & Overlay        PDF Medical Report Generation
         │                                   │
         └─────────────────┬─────────────────┘
                           │
                           ▼
               Interactive React Dashboard
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
ResNet50 Prediction
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

- Leveraged **Transfer Learning** with ResNet50 pretrained on ImageNet.
- Fine-tuned the backbone instead of training from scratch, significantly reducing training time.

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

ResNet50_final.keras
```

---

## Run Application

### 1. Start the FastAPI Backend

From the repository root:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API documentation is interactively available at:
- Swagger UI: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

### 2. Start the React Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

The React web application will be accessible at:
```text
http://localhost:5173
```

---

# 📸 Application Features

- AI-Powered Chest X-Ray Detection with ResNet50 Transfer Learning
- Drag & Drop Image Upload with Format Validation
- Real-Time Inference (< 2 seconds)
- Prediction Confidence & Multi-Class Probability Distribution
- Grad-CAM Explainable AI Visual Heatmap and Overlay
- Interactive Clinical Data Analytics & Model Comparison Charts
- Downloadable Structured Clinical PDF Diagnostic Reports
- Diagnostic History Session Tracker
- Modern Clinical Glassmorphism UI built with React & Tailwind CSS

---

# 📈 Future Roadmap

- [x] Grad-CAM Explainable AI Visualization
- [x] REST API with FastAPI
- [x] Production React + TypeScript Frontend
- [ ] Multi-Disease Chest X-Ray Detection
- [ ] DICOM File Format Support
- [ ] Role-Based User Authentication
- [ ] Cloud Deployment (AWS / Azure / GCP)
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
- Full-Stack AI Integration (React + FastAPI)
- Asynchronous API Design & CORS Management
- Grad-CAM Explainable AI Implementation
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

# 🙏 Acknowledgements

- **[Lovable](https://lovable.dev)**: The frontend user interface and web application design for MediVision AI were created and generated using Lovable.dev.
- **COVID-19 Radiography Database**: Researchers from Qatar University, University of Dhaka, and collaborators for curating the chest X-ray datasets.
- Open-source communities behind TensorFlow, FastAPI, React, OpenCV, and Tailwind CSS.

---

# 👨‍💻 Author

**Himakar Pisipati**

B.Tech Computer Science & Engineering

Passionate about Artificial Intelligence, Computer Vision, Deep Learning, and Full-Stack AI Applications.

---

⭐ **If you found this project interesting, consider giving it a star!**