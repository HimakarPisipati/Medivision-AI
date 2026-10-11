import type { ReactNode } from 'react';
import { ArrowUpRight, ShieldCheck, CircleHelp, RefreshCw, type LucideIcon } from 'lucide-react';
import { Link } from '@tanstack/react-router';
import { Button } from '@/components/ui/button';
import { useHealth } from '@/hooks/use-api';
export function PageHeading({ title, description, action }: { title: string; description: string; action?: ReactNode }) {
  return <div className="page-heading"><div><h1>{title}</h1><p>{description}</p></div>{action && <div className="heading-action">{action}</div>}</div>;
}
export function AnalyzeCTA({ label = 'Analyze New X-Ray', hero = false }: { label?: string; hero?: boolean }) {
  return <Button asChild size="lg" variant={hero ? 'hero' : 'default'}><Link to="/analyze">{label}<ArrowUpRight size={16}/></Link></Button>;
}
export function Panel({ title, icon: Icon, action, children, className = '' }: { title: string; icon?: LucideIcon; action?: ReactNode; children: ReactNode; className?: string }) {
  return <section className={`panel ${className}`}><div className="panel-header"><h2>{Icon && <Icon size={16} className="text-muted-foreground"/>}{title}</h2>{action}</div>{children}</section>;
}
export function EmptyState({ title, description, icon: Icon = CircleHelp, action, className = '' }: { title: string; description: string; icon?: LucideIcon; action?: ReactNode; className?: string }) {
  return <div className={`empty-state ${className}`}><div className="icon-well neutral"><Icon size={23}/></div><h3>{title}</h3><p>{description}</p>{action}</div>;
}
export function LoadingState() { return <div className="panel-body" role="status" aria-label="Loading"><div className="skeleton-line"/><div className="skeleton-line"/><div className="skeleton-line"/></div>; }
export function Retry({ retry }: { retry: () => unknown }) { return <Button variant="outline" size="sm" onClick={() => retry()}><RefreshCw/>Retry connection</Button>; }
export function BackendStatus() {
  const health = useHealth();
  const online = !!health.data && ['ok','healthy','ready','online'].includes(health.data.status.toLowerCase());
  const label = health.isPending ? 'Checking backend' : online ? health.data?.model_loaded === false ? 'Model not loaded' : 'Backend connected' : 'Backend offline';
  return <span className="status-chip" role="status"><span className={`status-dot ${online && health.data?.model_loaded !== false ? 'connected' : ''}`}/>{label}</span>;
}
export function Disclaimer() { return <div className="disclaimer"><ShieldCheck size={13}/><p><strong>For educational and research use only.</strong> MediVision AI is an AI-assisted screening prototype, not a clinically validated diagnostic system. Results should not be used for medical decisions.</p></div>; }
export function PageFooter() { return <footer className="page-footer"><span>© 2026 MediVision AI · Computer Vision Research</span><span><ShieldCheck size={11}/>Built for research. Designed with care.</span></footer>; }
export function percent(value?: number) { return value === undefined ? 'Not available' : `${(value * 100).toFixed(1)}%`; }
export function dateLabel(value?: string) { if (!value || Number.isNaN(new Date(value).getTime())) return 'Not available'; return new Date(value).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' }); }
