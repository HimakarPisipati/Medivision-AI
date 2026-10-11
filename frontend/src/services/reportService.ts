import { api, endpoints } from './api';
import type { Prediction } from '@/types/api';
export async function downloadReport(file: File, prediction: Prediction) {
  const body = new FormData(); body.append('file', file); body.append('prediction', JSON.stringify(prediction));
  if (prediction.analysis_id) body.append('analysis_id', prediction.analysis_id);
  const response = await api.post<Blob>(endpoints.report, body, { responseType: 'blob', timeout: 60000 });
  if (!String(response.headers['content-type'] || '').includes('application/pdf') || response.data.size === 0) throw new Error('The backend did not return a valid PDF report.');
  const signature = await response.data.slice(0, 5).text();
  if (signature !== '%PDF-') throw new Error('The backend did not return a valid PDF report.');
  const url = URL.createObjectURL(response.data); const a = document.createElement('a');
  a.href = url; a.download = `MediVision-${file.name.replace(/\.[^.]+$/, '')}.pdf`; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
