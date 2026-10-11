export const CLASSES = ['COVID', 'Normal', 'Viral Pneumonia'] as const;
export type DiseaseClass = (typeof CLASSES)[number];
export interface Prediction {
  predicted_class: DiseaseClass;
  confidence?: number | undefined;
  probabilities: Partial<Record<DiseaseClass, number>>;
  model_name?: string | undefined;
  analysis_id?: string | undefined;
  timestamp?: string | undefined;
  gradcam?: { heatmap_url?: string | null | undefined; overlay_url?: string | null | undefined };
  caution?: { threshold: number; message: string } | undefined;
}
export interface AnalysisRecord extends Prediction { id: string; filename: string; created_at?: string | undefined; image_url?: string | undefined }
export interface Health { status: string; model_loaded?: boolean | undefined }
export interface ModelInfo { model_name?: string | undefined; description?: string | undefined }
export interface Evaluation {
  metrics?: Partial<Record<'accuracy' | 'precision' | 'recall' | 'f1_score' | 'roc_auc' | 'training_time_min', number>>;
  training_time_min?: number | undefined;
  test_samples?: number | undefined;
  macro_avg?: { precision?: number; recall?: number; f1_score?: number } | undefined;
  weighted_avg?: { precision?: number; recall?: number; f1_score?: number } | undefined;
  confusion_matrix?: number[][] | undefined;
  class_metrics?: Partial<Record<DiseaseClass, { precision?: number | undefined; recall?: number | undefined; f1_score?: number | undefined; support?: number | undefined }>>;
  summary?: string | undefined;
}
export interface ModelComparison {
  model_name: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  roc_auc?: number | null | undefined;
  training_time_min?: number | null | undefined;
  is_best?: boolean | undefined;
}
