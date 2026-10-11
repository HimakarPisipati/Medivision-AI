import io
import os
import uuid
import json
import base64
import logging
from typing import Optional
from contextlib import asynccontextmanager

from PIL import Image
import numpy as np
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse

from utils.preprocessing import preprocess_image
from utils.predict import load_cached_model, predict_disease, CLASSES
from utils.gradcam import generate_gradcam
from utils.report_generator import generate_pdf_report

logger = logging.getLogger("medivision")
logging.basicConfig(level=logging.INFO)

# Root directory of project
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "ResNet50_final.keras")
COMPARISON_CSV = os.path.join(PROJECT_ROOT, "model_comparison", "model_comparison_summary.csv")

model_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_instance
    logger.info("Initializing MediVision AI backend and loading ResNet50 model...")
    try:
        model_instance = load_cached_model(MODEL_PATH)
        if model_instance is not None:
            logger.info("ResNet50 model loaded successfully.")
        else:
            logger.warning(f"ResNet50 model could not be loaded from {MODEL_PATH}.")
    except Exception as e:
        logger.error(f"Error during model startup: {e}", exc_info=True)
    yield
    logger.info("MediVision AI backend shutting down.")

app = FastAPI(
    title="MediVision AI API",
    description="Chest X-Ray Disease Detection and Clinical Explainability Backend",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def numpy_to_base64_data_url(img_array: np.ndarray, format: str = "PNG") -> str:
    """Converts an RGB or RGBA uint8 numpy image array to a base64 data URL."""
    pil_img = Image.fromarray(img_array.astype(np.uint8))
    buffer = io.BytesIO()
    pil_img.save(buffer, format=format)
    b64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/{format.lower()};base64,{b64_str}"

@app.get("/api/health")
async def health_check():
    """Health check endpoint confirming backend status and model availability."""
    global model_instance
    if model_instance is None:
        model_instance = load_cached_model(MODEL_PATH)

    is_loaded = model_instance is not None
    return {
        "status": "healthy" if is_loaded else "degraded",
        "model_loaded": is_loaded,
        "model_name": "ResNet50",
        "classes": CLASSES,
        "version": "1.0.0"
    }

@app.get("/api/model-info")
async def get_model_info():
    """Returns technical metadata, architecture details, and verification parameters."""
    return {
        "model_name": "ResNet50",
        "architecture": "ResNet50 (Fine-Tuned Transfer Learning)",
        "input_shape": [224, 224, 3],
        "num_classes": len(CLASSES),
        "classes": CLASSES,
        "dataset": "COVID-19 Radiography Database",
        "training_framework": "TensorFlow / Keras",
        "weights_path": "models/ResNet50_final.keras",
        "target_size": "224x224",
        "preprocessing": "Zero-centered ImageNet normalization (tf.keras.applications.resnet50.preprocess_input)",
        "training_time_min": 79.19051173130671,
        "metrics": {
            "accuracy": 0.9808959156785244,
            "precision": 0.9810326208506397,
            "recall": 0.9808959156785244,
            "f1_score": 0.9807989452919617,
            "roc_auc": 0.9979725384097238,
            "training_time_min": 79.19051173130671
        }
    }

@app.get("/api/evaluation")
async def get_evaluation():
    """Returns genuine evaluation results, per-class metrics, and confusion matrix."""
    return {
        "model_name": "ResNet50",
        "dataset": "COVID-19 Radiography Database",
        "test_samples": 1518,
        "accuracy": 0.9808959156785244,
        "precision": 0.9810326208506397,
        "recall": 0.9808959156785244,
        "f1": 0.9807989452919617,
        "f1_score": 0.9807989452919617,
        "auc": 0.9979725384097238,
        "roc_auc": 0.9979725384097238,
        "training_time_min": 79.19051173130671,
        "metrics": {
            "accuracy": 0.9808959156785244,
            "precision": 0.9810326208506397,
            "recall": 0.9808959156785244,
            "f1_score": 0.9807989452919617,
            "roc_auc": 0.9979725384097238,
            "training_time_min": 79.19051173130671
        },
        "macro_avg": {
            "precision": 0.977787,
            "recall": 0.978693,
            "f1_score": 0.977959
        },
        "weighted_avg": {
            "precision": 0.9810326208506397,
            "recall": 0.9808959156785244,
            "f1_score": 0.9807989452919617
        },
        "classes": CLASSES,
        "class_metrics": {
            "COVID": {
                "precision": 0.9885,
                "recall": 0.9449,
                "f1_score": 0.9662,
                "support": 363
            },
            "Normal": {
                "precision": 0.9806,
                "recall": 0.9912,
                "f1_score": 0.9859,
                "support": 1020
            },
            "Viral Pneumonia": {
                "precision": 0.9643,
                "recall": 1.0000,
                "f1_score": 0.9818,
                "support": 135
            }
        },
        "per_class": {
            "COVID": {
                "precision": 0.9885,
                "recall": 0.9449,
                "f1_score": 0.9662,
                "support": 363
            },
            "Normal": {
                "precision": 0.9806,
                "recall": 0.9912,
                "f1_score": 0.9859,
                "support": 1020
            },
            "Viral Pneumonia": {
                "precision": 0.9643,
                "recall": 1.0000,
                "f1_score": 0.9818,
                "support": 135
            }
        },
        "confusion_matrix": [
            [343, 20, 0],
            [4, 1011, 5],
            [0, 0, 135]
        ],
        "summary": (
            "ResNet50 demonstrated top classification performance across all test metrics, "
            "achieving 98.09% accuracy (0.980896), 98.10% precision, 98.09% recall, "
            "98.08% F1-score, and an ROC-AUC of 0.9980 (0.997973) with a training time of "
            "79.19 minutes on the 1,518 test images of the COVID-19 Radiography Database."
        ),
        "classification_report": (
            "                 precision    recall  f1-score   support\n\n"
            "          COVID     0.9885    0.9449    0.9662       363\n"
            "         Normal     0.9806    0.9912    0.9859      1020\n"
            "Viral Pneumonia     0.9643    1.0000    0.9818       135\n\n"
            "       accuracy                         0.9809      1518\n"
            "      macro avg     0.9778    0.9787    0.9780      1518\n"
            "   weighted avg     0.9810    0.9809    0.9808      1518"
        )
    }

@app.get("/api/comparison")
async def get_comparison():
    """Returns architectural comparison data from the verified model comparison benchmark."""
    models_list = []
    if os.path.exists(COMPARISON_CSV):
        try:
            df = pd.read_csv(COMPARISON_CSV)
            for _, row in df.iterrows():
                name = str(row.get("Model", ""))
                models_list.append({
                    "model_name": name,
                    "accuracy": float(row.get("Accuracy", 0.0)),
                    "precision": float(row.get("Precision", 0.0)),
                    "recall": float(row.get("Recall", 0.0)),
                    "f1_score": float(row.get("F1 Score", 0.0)),
                    "roc_auc": float(row.get("ROC-AUC", 0.0)) if pd.notnull(row.get("ROC-AUC")) else None,
                    "training_time_min": float(row.get("Training Time (min)", 0.0)) if pd.notnull(row.get("Training Time (min)")) else None,
                    "is_best": bool(name == "ResNet50")
                })
        except Exception as e:
            logger.error(f"Error parsing comparison CSV: {e}")

    if not models_list:
        models_list = [
            {"model_name": "ResNet50", "accuracy": 0.9808959156785244, "precision": 0.9810326208506397, "recall": 0.9808959156785244, "f1_score": 0.9807989452919617, "roc_auc": 0.9979725384097238, "training_time_min": 79.19051173130671, "is_best": True},
            {"model_name": "Xception", "accuracy": 0.9644268774703557, "precision": 0.9644860984199056, "recall": 0.9644268774703557, "f1_score": 0.9640862786411305, "roc_auc": 0.9940853385591071, "training_time_min": 70.83585867881774, "is_best": False},
            {"model_name": "MobileNetV2", "accuracy": 0.9591567852437418, "precision": 0.9592281888135351, "recall": 0.9591567852437418, "f1_score": 0.9591882394993456, "roc_auc": 0.9947019239546364, "training_time_min": 108.57681167523066, "is_best": False},
            {"model_name": "DenseNet121", "accuracy": 0.9499341238471674, "precision": 0.9496820965209705, "recall": 0.9499341238471674, "f1_score": 0.9495480968138906, "roc_auc": 0.9880173773050914, "training_time_min": 105.61363939841588, "is_best": False},
            {"model_name": "EfficientNetB0", "accuracy": 0.932806324110672, "precision": 0.9394850539201793, "recall": 0.932806324110672, "f1_score": 0.9341404182787924, "roc_auc": 0.9897144761324689, "training_time_min": 125.10777802467346, "is_best": False}
        ]

    return {"models": models_list}

@app.post("/api/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    Accepts a chest X-ray image (PNG, JPEG), runs genuine ResNet50 inference,
    generates Grad-CAM visual explainability maps, and returns diagnostic results.
    """
    global model_instance
    if model_instance is None:
        model_instance = load_cached_model(MODEL_PATH)
        if model_instance is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model weights could not be loaded."
            )

    # Validate file extension and content
    filename = file.filename or "upload"
    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".png", ".jpg", ".jpeg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload a PNG or JPEG chest X-ray image."
        )

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty."
        )

    if len(file_bytes) > 20 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum allowed limit of 20 MB."
        )

    # Open PIL image for Grad-CAM overlay
    try:
        pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to decode uploaded image: {str(e)}"
        )

    # Preprocess image tensor for ResNet50
    try:
        img_tensor = preprocess_image(io.BytesIO(file_bytes))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during image preprocessing: {str(e)}"
        )

    # Model inference
    try:
        predicted_class, raw_conf, probs, inference_time = predict_disease(model_instance, img_tensor)
        pred_idx = CLASSES.index(predicted_class)
        # Probabilities as floats between 0.0 and 1.0
        prob_dict = {cls_name: float(probs[i]) for i, cls_name in enumerate(CLASSES)}
        confidence_float = float(probs[pred_idx])
    except Exception as e:
        logger.error(f"Inference error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during model inference: {str(e)}"
        )

    # Grad-CAM heatmap and overlay generation
    gradcam_data = None
    try:
        heatmap_rgb, overlay_rgb = generate_gradcam(
            model=model_instance,
            input_image=img_tensor,
            predicted_index=pred_idx,
            original_image=pil_img
        )
        gradcam_data = {
            "heatmap_url": numpy_to_base64_data_url(heatmap_rgb),
            "overlay_url": numpy_to_base64_data_url(overlay_rgb)
        }
    except Exception as e:
        logger.warning(f"Grad-CAM generation failed: {e}", exc_info=True)

    analysis_id = uuid.uuid4().hex[:12]

    # Clinical caution indicator if top prediction confidence is below clinical threshold
    caution_payload = None
    if confidence_float < 0.60:
        caution_payload = {
            "threshold": 0.60,
            "message": "Prediction confidence is below 60%. Secondary clinical verification recommended."
        }

    return {
        "analysis_id": analysis_id,
        "model_name": "ResNet50",
        "predicted_class": predicted_class,
        "confidence": confidence_float,
        "probabilities": prob_dict,
        "inference_time_ms": round(inference_time * 1000, 1),
        "gradcam": gradcam_data,
        "caution": caution_payload
    }

@app.post("/api/report")
async def generate_report(
    file: UploadFile = File(...),
    prediction: str = Form(...),
    analysis_id: Optional[str] = Form(None)
):
    """
    Generates a structured clinical PDF diagnostic report using ReportLab
    and returns it as a downloadable attachment.
    """
    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Missing or empty image file.")

    try:
        pred_data = json.loads(prediction)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid prediction payload: {str(e)}")

    predicted_class = pred_data.get("predicted_class", "Unknown")
    confidence = pred_data.get("confidence", 0.0)
    # Convert confidence to percentage scale [0, 100] as expected by ReportLab generator
    if confidence <= 1.0:
        conf_pct = float(confidence) * 100.0
    else:
        conf_pct = float(confidence)

    probs_raw = pred_data.get("probabilities", {})
    if isinstance(probs_raw, dict):
        prob_list = [float(probs_raw.get(c, 0.0)) for c in CLASSES]
    elif isinstance(probs_raw, list):
        prob_list = [float(p) for p in probs_raw]
    else:
        prob_list = [0.0, 0.0, 0.0]

    inf_time_ms = pred_data.get("inference_time_ms", 50.0)
    inf_time_sec = float(inf_time_ms) / 1000.0

    try:
        pdf_bytes = generate_pdf_report(
            image_file=io.BytesIO(file_bytes),
            predicted_class=predicted_class,
            confidence=conf_pct,
            probabilities=prob_list,
            inference_time=inf_time_sec
        )
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Report generation error: {str(e)}")

    safe_id = analysis_id or "report"
    filename = f"MediVision-Report-{predicted_class}-{safe_id}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
