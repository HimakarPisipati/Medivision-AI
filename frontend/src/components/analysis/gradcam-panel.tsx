import { useState } from 'react';
import { ScanLine, Columns2, Info } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Panel, EmptyState } from '@/components/shared/common';
import type { Prediction } from '@/types/api';
export function MedicalImage({ src, label }: { src: string; label: string }) {
  const [failed, setFailed] = useState(false);
  return failed ? <EmptyState icon={ScanLine} title="Image unavailable" description={`${label} could not be loaded from the backend.`}/> : <div className="gradcam-image"><img src={src} alt={label} onError={() => setFailed(true)}/></div>;
}
export function GradcamPanel({ original, result }: { original: string; result: Prediction }) {
  const [view, setView] = useState<'original'|'heatmap'|'overlay'>('original');
  const [compare, setCompare] = useState(false);
  const source = view === 'original' ? original : view === 'heatmap' ? result.gradcam?.heatmap_url : result.gradcam?.overlay_url;
  const label = view === 'original' ? 'Original X-ray' : view === 'heatmap' ? 'Grad-CAM heatmap' : 'Grad-CAM overlay';
  return <Panel className="gradcam-panel" title="A closer look with Grad-CAM" icon={ScanLine} action={<div className="flex gap-3 items-center flex-wrap"><div className="segmented" aria-label="Visualization view">{(['original','heatmap','overlay'] as const).map(mode => <Button key={mode} size="sm" variant="ghost" aria-pressed={view === mode} onClick={() => setView(mode)}>{mode === 'original' ? 'Original' : mode === 'heatmap' ? 'Heatmap' : 'Overlay'}</Button>)}</div><Button variant="outline" size="icon" title="Compare side by side" aria-label="Compare side by side" aria-pressed={compare} onClick={() => setCompare(!compare)}><Columns2/></Button></div>}><div className="panel-body"><div className={`gradcam-views ${compare ? 'compare' : ''}`}>{compare && <div><MedicalImage src={original} label="Original chest X-ray"/><p className="gradcam-caption">Original X-ray</p></div>}<div>{source ? <MedicalImage key={source} src={source} label={label}/> : <EmptyState icon={ScanLine} title="Visualization not available" description="The backend did not return this Grad-CAM image. Your prediction results are still available."/>}<p className="gradcam-caption">{label}</p></div></div><div className="inline-note"><Info size={15}/><p>Grad-CAM highlights image regions that influenced the model's prediction. These visualizations support model interpretability but do not establish medical correctness.</p></div></div></Panel>;
}
