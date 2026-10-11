import { createFileRoute } from '@tanstack/react-router';
import { AboutPage } from '@/features/about-page';
import { pageHead } from '@/lib/page-head';
export const Route = createFileRoute('/about')({ head: () => pageHead('About the Project', 'Learn about MediVision AI, the COVID-19 Radiography Database, ResNet50, the Python pipeline, and educational limitations.'), component: AboutPage });
