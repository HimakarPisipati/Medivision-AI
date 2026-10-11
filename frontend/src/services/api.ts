import axios from 'axios';
export const API_BASE_URL = import.meta.env['VITE_API_BASE_URL'] || 'http://localhost:8000';
export const endpoints = { health: '/api/health', predict: '/api/predict', report: '/api/report', history: '/api/history', model: '/api/model-info', evaluation: '/api/evaluation', comparison: '/api/comparison' } as const;
export const api = axios.create({ baseURL: API_BASE_URL, timeout: 15000 });
export function apiError(error: unknown): string {
  if (error instanceof Error && error.message.startsWith('Invalid API')) return error.message;
  if (axios.isAxiosError(error)) {
    if (error.code === 'ERR_CANCELED') return 'Analysis canceled. You can try again.';
    if (error.code === 'ECONNABORTED') return 'The request timed out. Please check the backend and try again.';
    if (!error.response) return 'Unable to reach the FastAPI backend. Check that it is running and allows this application to connect.';
    if (error.response.status === 404) return 'This endpoint is not connected yet.';
    if (error.response.status === 413) return 'This image is too large for the backend. Please choose a smaller image.';
    if (error.response.status === 415 || error.response.status === 422 || error.response.status === 400) return 'The backend could not process this image. Please choose a valid PNG or JPEG chest X-ray.';
    if (error.response.status === 503) return 'The model is not ready. Please check that ResNet50 has loaded on the backend.';
    return 'The backend could not complete this request. Please try again.';
  }
  return error instanceof Error ? error.message : 'Something went wrong. Please try again.';
}
export function assetUrl(value?: string | null): string | undefined {
  if (!value) return undefined;
  if (/^data:image\/(png|jpeg|webp);base64,/.test(value)) return value;
  try { const url = new URL(value, API_BASE_URL); return ['http:', 'https:'].includes(url.protocol) ? url.href : undefined; } catch { return undefined; }
}
