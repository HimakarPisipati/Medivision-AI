import { api, endpoints, assetUrl } from './api';
import { CLASSES, type Prediction } from '@/types/api';
export const validProbability = (value: unknown): value is number => typeof value === 'number' && Number.isFinite(value) && value >= 0 && value <= 1;
export function adaptPrediction(data: unknown): Prediction {
  if (!data || typeof data !== 'object') throw new Error('Invalid API response: no prediction was returned.');
  const d = data as Record<string, unknown>;
  if (!CLASSES.includes(d['predicted_class'] as Prediction['predicted_class'])) throw new Error('Invalid API response: the predicted class is not supported.');
  const probs = d['probabilities'] && typeof d['probabilities'] === 'object' ? d['probabilities'] as Record<string, unknown> : {};
  const probabilities: Prediction['probabilities'] = {};
  for (const name of CLASSES) if (validProbability(probs[name])) probabilities[name] = probs[name];
  const g = d['gradcam'] && typeof d['gradcam'] === 'object' ? d['gradcam'] as Record<string, unknown> : {};
  const caution = d['caution'] as { threshold?: unknown; message?: unknown } | undefined;
  return {
    predicted_class: d['predicted_class'] as Prediction['predicted_class'],
    confidence: validProbability(d['confidence']) ? d['confidence'] : undefined,
    probabilities,
    model_name: typeof d['model_name'] === 'string' ? d['model_name'] : undefined,
    analysis_id: typeof d['analysis_id'] === 'string' ? d['analysis_id'] : undefined,
    timestamp: typeof d['timestamp'] === 'string' ? d['timestamp'] : undefined,
    gradcam: { heatmap_url: typeof g['heatmap_url'] === 'string' ? assetUrl(g['heatmap_url']) : undefined, overlay_url: typeof g['overlay_url'] === 'string' ? assetUrl(g['overlay_url']) : undefined },
    caution: caution && validProbability(caution.threshold) && typeof caution.message === 'string' ? { threshold: caution.threshold, message: caution.message } : undefined,
  };
}
export async function predictImage(file: File, signal?: AbortSignal): Promise<Prediction> {
  const body = new FormData(); body.append('file', file);
  const { data } = await api.post(endpoints.predict, body, { ...(signal ? { signal } : {}), timeout: 120000 });
  return adaptPrediction(data);
}
