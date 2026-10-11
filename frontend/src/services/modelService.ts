import { api, endpoints } from './api';
import { validProbability } from './predictionService';
import { CLASSES, type Evaluation, type Health, type ModelInfo, type ModelComparison } from '@/types/api';
export async function getHealth(): Promise<Health> {
  const { data } = await api.get(endpoints.health, { timeout: 5000 });
  if (!data || typeof data.status !== 'string') throw new Error('Invalid API response: backend health is unavailable.');
  return { status: data.status, model_loaded: typeof data.model_loaded === 'boolean' ? data.model_loaded : undefined };
}
export async function getModelInfo(): Promise<ModelInfo> {
  const { data } = await api.get(endpoints.model);
  if (!data || typeof data !== 'object') throw new Error('Invalid API response: model information is unavailable.');
  return { model_name: typeof data.model_name === 'string' ? data.model_name : undefined, description: typeof data.description === 'string' ? data.description : undefined };
}
export async function getEvaluation(): Promise<Evaluation> {
  const { data } = await api.get(endpoints.evaluation);
  if (!data || typeof data !== 'object') throw new Error('Invalid API response: evaluation data is unavailable.');
  const metrics: NonNullable<Evaluation['metrics']> = {};
  for (const key of ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc'] as const) {
    const rawVal = data.metrics?.[key] ?? data[key] ?? (key === 'f1_score' ? (data.metrics?.f1 ?? data.f1) : undefined) ?? (key === 'roc_auc' ? (data.metrics?.auc ?? data.auc) : undefined);
    if (validProbability(rawVal)) metrics[key] = rawVal;
  }
  const trainingTime = typeof data.training_time_min === 'number' ? data.training_time_min : typeof data.metrics?.training_time_min === 'number' ? data.metrics.training_time_min : undefined;
  if (trainingTime !== undefined) metrics.training_time_min = trainingTime;

  const matrix = data.confusion_matrix;
  const class_metrics: NonNullable<Evaluation['class_metrics']> = {};
  const rawClassData = data.class_metrics || data.per_class || {};
  for (const name of CLASSES) {
    const row = rawClassData[name];
    if (row) {
      class_metrics[name] = {
        precision: validProbability(row.precision) ? row.precision : undefined,
        recall: validProbability(row.recall) ? row.recall : undefined,
        f1_score: validProbability(row.f1_score ?? row.f1) ? (row.f1_score ?? row.f1) : undefined,
        support: typeof row.support === 'number' ? row.support : undefined,
      };
    }
  }

  return {
    metrics,
    training_time_min: trainingTime,
    test_samples: typeof data.test_samples === 'number' ? data.test_samples : undefined,
    macro_avg: data.macro_avg,
    weighted_avg: data.weighted_avg,
    class_metrics,
    confusion_matrix: Array.isArray(matrix) && matrix.length === 3 && matrix.every((r: unknown) => Array.isArray(r) && r.length === 3 && r.every((v: unknown) => typeof v === 'number' && Number.isInteger(v) && v >= 0)) ? matrix : undefined,
    summary: typeof data.summary === 'string' ? data.summary : undefined
  };
}
export async function getComparison(): Promise<{ models: ModelComparison[] }> {
  const { data } = await api.get(endpoints.comparison);
  if (!data || !Array.isArray(data.models)) throw new Error('Invalid API response: comparison data is unavailable.');
  return {
    models: data.models.map((m: Record<string, unknown>) => ({
      model_name: String(m['model_name'] || ''),
      accuracy: Number(m['accuracy'] ?? 0),
      precision: Number(m['precision'] ?? 0),
      recall: Number(m['recall'] ?? 0),
      f1_score: Number(m['f1_score'] ?? 0),
      roc_auc: typeof m['roc_auc'] === 'number' ? m['roc_auc'] : null,
      training_time_min: typeof m['training_time_min'] === 'number' ? m['training_time_min'] : null,
      is_best: Boolean(m['is_best']),
    }))
  };
}

