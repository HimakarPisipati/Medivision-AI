import { createFileRoute } from '@tanstack/react-router';
import { DashboardPage } from '@/components/dashboard/dashboard-page';
import { pageHead } from '@/lib/page-head';
export const Route = createFileRoute('/dashboard')({ head: () => pageHead('Research Overview', 'Explore MediVision AI chest X-ray screening, ResNet50, and interpretable image analysis.'), component: DashboardPage });
