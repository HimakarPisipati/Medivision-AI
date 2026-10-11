import { useEffect, useRef, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useQueryClient } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { Upload, ScanLine, ImagePlus, FileImage, X, BrainCircuit, ArrowRight, ShieldCheck, Check, Info, LoaderCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Panel, PageHeading, EmptyState, Disclaimer, PageFooter } from '@/components/shared/common';
import { validateImage, readImage, MAX_IMAGE_BYTES } from '@/lib/upload';
import { predictImage } from '@/services/predictionService';
import { apiError } from '@/services/api';
import type { Prediction } from '@/types/api';
import { PredictionResult } from './prediction-result';
import { GradcamPanel } from './gradcam-panel';
interface UploadImage { file: File; url: string; width: number; height: number }
export function AnalyzePage() {
  const [image, setImage] = useState<UploadImage>();
  const [result, setResult] = useState<Prediction>();
  const [error, setError] = useState('');
  const [processing, setProcessing] = useState(false);
  const [reading, setReading] = useState(false);
  const request = useRef<AbortController | undefined>(undefined);
  const selection = useRef(0);
  const queryClient = useQueryClient();
  useEffect(() => () => { request.current?.abort(); selection.current += 1; }, []);
  useEffect(() => () => { if (image) URL.revokeObjectURL(image.url); }, [image]);
  async function selectFile(files: File[]) {
    const file = files[0]; if (!file) return;
    const validation = validateImage(file); if (validation) { setError(validation); return; }
    const current = ++selection.current; setError(''); setReading(true); setResult(undefined);
    try { const preview = await readImage(file); if (current !== selection.current) { URL.revokeObjectURL(preview.url); return; } setImage({ file, ...preview }); } catch (err) { if (current === selection.current) setError(apiError(err)); } finally { if (current === selection.current) setReading(false); }
  }
  const dropzone = useDropzone({ onDropAccepted: selectFile, onDropRejected: rejected => setError(rejected[0]?.errors.some(e => e.code === 'file-too-large') ? 'Please choose an image smaller than 20 MB.' : 'Choose one PNG, JPG, or JPEG image.'), accept: { 'image/png': ['.png'], 'image/jpeg': ['.jpg','.jpeg'] }, maxSize: MAX_IMAGE_BYTES, maxFiles: 1, multiple: false, noClick: true, noKeyboard: true, disabled: processing || reading });
  function reset() { request.current?.abort(); selection.current += 1; setImage(undefined); setResult(undefined); setError(''); setProcessing(false); setReading(false); }
  async function analyze() {
    if (!image || processing) return;
    const controller = new AbortController(); request.current = controller;
    setProcessing(true); setError(''); setResult(undefined);
    try { const output = await predictImage(image.file, controller.signal); if (!controller.signal.aborted) { setResult(output); } } catch (err) { if (!controller.signal.aborted) setError(apiError(err)); } finally { if (request.current === controller) setProcessing(false); }
  }
  function cancel() { request.current?.abort(); setProcessing(false); setError('Analysis canceled. The backend may still finish processing this request.'); }
  return <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .25 }}><PageHeading title="Analyze a chest X-ray" description="Bring your image. Let the model reveal its perspective." action={<span className="tag"><BrainCircuit size={12}/>ResNet50 · 3 classes</span>}/><div className="analysis-grid"><div><Panel title="X-ray image" icon={FileImage} action={<span className="text-[9px] text-muted-foreground">STEP 01 · UPLOAD</span>}><div className="panel-body"><input {...dropzone.getInputProps()} aria-label="Upload chest X-ray"/>{image ? <><div className="image-preview"><img src={image.url} alt="Uploaded chest X-ray preview"/>{processing && <div className="scan-line"/>}</div><div className="file-detail"><div className="icon-well"><FileImage size={19}/></div><div className="flex-1 min-w-0"><strong>{image.file.name}</strong><p>{image.width} × {image.height} px · {(image.file.size / 1024 / 1024).toFixed(2)} MB · {image.file.type.split('/')[1]?.toUpperCase()}</p></div><Button variant="ghost" size="icon" onClick={reset} disabled={processing} title="Remove image" aria-label="Remove image"><X/></Button></div><Button variant="link" size="sm" onClick={dropzone.open} disabled={processing || reading} className="mt-3 p-0"><ImagePlus/>Replace image</Button></> : <div {...dropzone.getRootProps()} className={`upload-zone ${dropzone.isDragActive ? 'active' : ''}`}><div className="upload-icon">{reading ? <LoaderCircle size={28} className="animate-spin"/> : <Upload size={28}/>}</div><h3>{reading ? 'Opening your image…' : dropzone.isDragActive ? 'Drop your X-ray here' : 'Drag & drop your chest X-ray'}</h3><p>or choose an image from your computer</p><Button variant="outline" onClick={dropzone.open} disabled={reading} className="mt-5"><ImagePlus/>Browse files</Button><div className="upload-requirements"><span><Check size={10}/>PNG, JPG, JPEG</span><span><Check size={10}/>Up to 20 MB</span></div></div>}{error && <div role="alert" className="alert-error">{error}</div>}</div><div className="analysis-action"><Button size="lg" onClick={analyze} disabled={!image || processing || reading}>{processing ? <LoaderCircle className="animate-spin"/> : <BrainCircuit/>}{processing ? 'Analyzing image…' : 'Analyze Image'}{!processing && <ArrowRight/>}</Button><p><ShieldCheck size={12}/>Your image is sent only when you start the analysis.</p></div></Panel><div className="inline-note"><Info size={16}/><p>Use a chest X-ray image for this model. Validation checks the file format—not whether the image is a medically suitable X-ray. Preprocessing takes place on the Python backend.</p></div></div><div>{result && image ? <PredictionResult result={result} file={image.file} onReset={reset}/> : <Panel title="Analysis results" icon={ScanLine} action={<span className="text-[9px] text-muted-foreground">STEP 02 · INSIGHTS</span>}>{processing ? <div className="empty-state result-placeholder" role="status"><div className="processing-ring"/><h3>Looking beneath the surface</h3><p>The backend is processing your image with ResNet50. Results will appear when analysis is complete.</p><Button size="sm" variant="outline" onClick={cancel}><X/>Cancel request</Button></div> : <EmptyState className="result-placeholder" icon={ScanLine} title="A new perspective awaits" description="Upload a chest X-ray and start an analysis to explore the model’s prediction." action={<div className="result-steps"><span className="tag">Class prediction</span><span className="tag">Probabilities</span><span className="tag">Grad-CAM</span></div>}/>}</Panel>}<div className="inline-note"><BrainCircuit size={16}/><p><strong className="text-foreground">One model. Three possible classes.</strong><br/>COVID, Normal, and Viral Pneumonia. Predictions reflect the trained model’s output, not a medical diagnosis.</p></div></div></div>{result && image && <GradcamPanel original={image.url} result={result}/>}<Disclaimer/><PageFooter/></motion.div>;
}
