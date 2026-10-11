import { createFileRoute } from '@tanstack/react-router';
import { ModelInsightsPage } from '@/features/model-insights-page';
import { pageHead } from '@/lib/page-head';
export const Route = createFileRoute('/model-insights')({ head: () => pageHead('Model Insights', 'Inspect the ResNet50 architecture and verified test-set metrics, confusion matrix, and Grad-CAM interpretability.'), component: ModelInsightsPage });
