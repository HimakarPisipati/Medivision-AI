import { createFileRoute } from '@tanstack/react-router';
import { AnalyzePage } from '@/components/analysis/analyze-page';
import { pageHead } from '@/lib/page-head';
export const Route = createFileRoute('/analyze')({ head: () => pageHead('Analyze Chest X-Ray', 'Upload a chest X-ray for ResNet50 prediction, class probabilities, Grad-CAM explanation, and a PDF report.'), component: AnalyzePage });
