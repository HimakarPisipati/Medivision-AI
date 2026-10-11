import { api, endpoints, assetUrl } from './api';
import { adaptPrediction } from './predictionService';
import type { AnalysisRecord } from '@/types/api';
export async function getHistory(): Promise<AnalysisRecord[]> {
  const { data } = await api.get(endpoints.history);
  const rows = Array.isArray(data) ? data : data?.analyses;
  if (!Array.isArray(rows)) throw new Error('Invalid API response: history could not be read.');
  return rows.map((row: Record<string, unknown>) => {
    if (typeof row['id'] !== 'string' || typeof row['filename'] !== 'string') throw new Error('Invalid API response: a history record is incomplete.');
    return { ...adaptPrediction(row), id: row['id'], filename: row['filename'], created_at: typeof row['created_at'] === 'string' ? row['created_at'] : undefined, image_url: typeof row['image_url'] === 'string' ? assetUrl(row['image_url']) : undefined };
  });
}
