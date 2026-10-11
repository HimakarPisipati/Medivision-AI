import { createFileRoute, redirect } from '@tanstack/react-router';
import { pageHead } from '@/lib/page-head';
export const Route = createFileRoute('/')({
  head: () => pageHead('MediVision AI', 'AI-powered chest X-ray screening research workspace.'),
  beforeLoad: () => { throw redirect({ to: '/dashboard' }); },
});
