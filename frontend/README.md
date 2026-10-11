# MediVision AI

AI-Powered Chest X-Ray Disease Detection System. A React 19 + TypeScript research frontend with a midnight navigation shell and bright analysis workspace. No simulated predictions, evaluation metrics, medical scans, Grad-CAM, or reports.

## Run locally

```sh
npm install
cp .env.example .env
npm run dev
```

Set `VITE_API_BASE_URL` in `.env` to your FastAPI origin (default `http://localhost:8000`). Restart Vite after changing environment variables. `npm run build`, `npm run preview`, and `npm test` are standard production, preview, and test commands. The Lovable template uses TanStack Start / TanStack Router rather than React Router, preserving its existing Vite bootstrap and SSR support.

## Pages

`/` redirects to `/dashboard`. Other pages: `/analyze`, `/history`, `/model-insights`, `/about`.

## Architecture

- `src/services`: centralized Axios instance, endpoint paths, response adapters, prediction / PDF / health / history / evaluation calls.
- `src/types/api.ts`: class order and typed contracts.
- `src/components/layout`: shared collapsible application shell.
- `src/components/analysis`: upload, results, actual Grad-CAM images, binary report download.
- `src/features`: history, model insights, project information.
- `src/hooks/use-api.ts`: React Query connection and optional endpoint states.
- `src/routes`: file-based navigation and page-specific metadata.
- `src/styles.css`: semantic design tokens and responsive layouts.

No database, authentication service, keys, or new inference backend is introduced. Python implementation is not included because the existing model and utilities were not supplied.

## FastAPI integration contract (proposed, not verified)

Centralized paths are in `src/services/api.ts`. All requests run in the browser and go directly to `VITE_API_BASE_URL`. Configure FastAPI CORS to allow your local Vite origin and deployed frontend origin. HTTPS hosting requires an HTTPS backend reachable from the browser; localhost targets the viewer's own computer. Do not place API secrets in VITE variables.

- `GET /api/health`: `{ "status": "ok", "model_loaded": true }`. Status values `ok`, `healthy`, `ready`, `online` are healthy. Health timeout: 5 seconds, polling every 30 seconds. Any other status is not shown as connected; a false `model_loaded` is shown separately.
- `POST /api/predict`: multipart `file`. Returns `predicted_class` (exactly COVID / Normal / Viral Pneumonia), optional `confidence` in [0,1], `probabilities` keyed in that exact class order, optional `model_name`, `analysis_id`, `timestamp`, `gradcam: { heatmap_url, overlay_url }`. No automatic submission on upload. Timeout: 120 seconds. Unsupported classes are rejected; missing/invalid numeric values appear as unavailable, never invented. Prediction labels are never recomputed from probabilities. Optional backend `caution: { threshold: number in [0,1], message: string }` supplies both the threshold and its semantics. No default threshold is applied.
- Grad-CAM accepts HTTP(S) URLs (relative to API origin) or `data:image/png;base64,...`, JPEG or WebP data URLs. Adapt `adaptPrediction` for other explicitly documented backend formats. No fake attention maps. URL failures and missing images have honest empty states.
- `POST /api/report`: multipart `file`, `prediction` JSON string containing the returned prediction, and optional `analysis_id`. Timeout: 60 seconds. Backend must return a non-empty `application/pdf` binary with a `%PDF-` signature. Use the existing ReportLab pipeline. Modify this adapter if your endpoint accepts only an identifier or a different form field. The browser downloads the returned binary; it does not build a PDF.
- `GET /api/history` (optional): an array or `{ "analyses": [...] }`. Each record includes string `id`, `filename`, prediction fields, optional `created_at`, `image_url`. No frontend persistence is assumed. Search, class filtering, valid date sorting, and an inspection dialog are included. Historical PDF downloads need the backend's retained original file / identifier contract and are not requested without one.
- `GET /api/model-info` (optional): `{ "model_name": "ResNet50", "description": "..." }`. Unavailable live model metadata is labeled; static architecture facts are from the project brief.
- `GET /api/evaluation` (optional): `{ "metrics": { "accuracy": ..., "precision": ..., "recall": ..., "f1_score": ..., "roc_auc": ... }, "confusion_matrix": [[...],[...],[...]], "class_metrics": { "COVID": {"precision": ..., "recall": ..., "f1_score": ...}, ... }, "summary": "..." }`. Metrics use [0,1], confusion matrix uses 3 × 3 nonnegative integer counts in COVID / Normal / Viral Pneumonia order. Rows actual, columns predicted. Provide only verified test-set data.

General requests time out after 15 seconds. Errors are translated into safe messages; server traceback text is never displayed. Browser cancel aborts the request, not necessarily Python inference. The upload limit is a frontend safety default of 20 MB, centralized in `src/lib/upload.ts`, not a medical suitability check. The backend must enforce its own file limits and validate actual image content.

## Existing Python compatibility

Keep `models/ResNet50_final.keras`, the 224 × 224 RGB pipeline, `tf.keras.applications.resnet50.preprocess_input`, exact class order `["COVID", "Normal", "Viral Pneumonia"]`, Grad-CAM utilities, and ReportLab utilities unchanged. FastAPI should call those existing functions. No training or JavaScript model preprocessing is implemented.

## Verification

Run `npm test` for upload validation and prediction adapter tests. For a real end-to-end check, start your FastAPI service, upload an actual chest X-ray, click Analyze Image, check backend values and Grad-CAM, and request the PDF. Optional history/evaluation features remain available with transparent disconnected states. A decorative digital lung illustration is explicitly labeled conceptual, not a clinical scan or sample image.

## Use limitations

Educational and research use only. Not clinically validated; not for medical decisions. Confidence for one prediction is not test-set accuracy. No clinical thresholds or external validation are asserted.
