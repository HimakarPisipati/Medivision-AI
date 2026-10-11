import { Link } from '@tanstack/react-router';
import { motion } from 'framer-motion';
import {
  ArrowRight,
  BrainCircuit,
  ScanLine,
  Upload,
  Layers3,
  ShieldCheck,
  Sparkles,
  Check,
  Cpu,
  Workflow,
  Eye,
  Activity,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  PageHeading,
  AnalyzeCTA,
  Panel,
  Disclaimer,
  PageFooter,
} from '@/components/shared/common';
import lungIllustration from '@/assets/lung-illustration.jpg';

const workflow = [
  {
    number: '01',
    icon: Upload,
    title: 'Upload a chest X-ray',
    description: 'Start with a PNG or JPEG image. Preview your X-ray before submitting it for analysis.',
  },
  {
    number: '02',
    icon: BrainCircuit,
    title: 'Let AI take a closer look',
    description: 'The fine-tuned ResNet50 model analyzes the image and returns a verified three-class prediction.',
  },
  {
    number: '03',
    icon: ScanLine,
    title: 'Understand the prediction',
    description: 'Explore class probabilities, inspect Grad-CAM attention heatmaps, and download a research report.',
  },
];

export function DashboardPage() {
  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
      <PageHeading
        title="A clearer view. A smarter analysis."
        description="Welcome to MediVision AI, your intelligent chest X-ray research workspace."
        action={<AnalyzeCTA />}
      />

      <section className="dashboard-hero">
        <img
          src={lungIllustration}
          alt="Conceptual digital lung illustration, not a medical scan"
          width={1200}
          height={800}
        />
        <div className="hero-content">
          <div className="eyebrow">
            <Sparkles size={12} />
            AI-powered medical imaging
          </div>
          <h2>
            Chest X-ray analysis.<br />
            <span>With a layer of understanding.</span>
          </h2>
          <p>
            Explore the potential of deep learning in chest X-ray screening. One image. Three classes. Interpretable insights.
          </p>
          <div className="hero-actions">
            <AnalyzeCTA label="Start an Analysis" hero />
            <Button
              variant="ghost"
              asChild
              className="text-shell-foreground hover:bg-shell-foreground/10 hover:text-shell-foreground text-[10px]"
            >
              <Link to="/model-insights">
                Explore the model <ArrowRight />
              </Link>
            </Button>
          </div>
          <div className="hero-class-list">
            {['COVID', 'Normal', 'Viral Pneumonia'].map(name => (
              <span key={name}>
                <Check size={10} />
                {name}
              </span>
            ))}
          </div>
        </div>
        <span className="hero-image-label">CONCEPTUAL LUNG VISUALIZATION · NOT A CLINICAL IMAGE</span>
      </section>

      <div className="summary-grid">
        <div className="info-tile">
          <div className="icon-well">
            <BrainCircuit size={21} />
          </div>
          <div>
            <h3>Powered by ResNet50</h3>
            <p>98.09% verified test accuracy.</p>
          </div>
        </div>
        <div className="info-tile">
          <div className="icon-well">
            <Layers3 size={21} />
          </div>
          <div>
            <h3>Three-class classification</h3>
            <p>COVID · Normal · Viral Pneumonia</p>
          </div>
        </div>
        <div className="info-tile">
          <div className="icon-well">
            <ScanLine size={21} />
          </div>
          <div>
            <h3>Explainable by design</h3>
            <p>Grad-CAM highlights key pulmonary regions.</p>
          </div>
        </div>
      </div>

      <div className="section-heading">
        <div>
          <h2>From image to insight</h2>
          <p>A focused workflow, built around your analysis.</p>
        </div>
        <span className="tag">
          <Workflow size={10} />3 simple steps
        </span>
      </div>

      <div className="workflow-grid">
        {workflow.map(step => (
          <article className="workflow-card" key={step.number}>
            <span className="step-number">{step.number}</span>
            <div className="icon-well">
              <step.icon size={20} />
            </div>
            <div>
              <h3>{step.title}</h3>
              <p>{step.description}</p>
            </div>
          </article>
        ))}
      </div>

      <div className="dashboard-bottom">
        <Panel title="Behind the intelligence" icon={Cpu} action={<span className="tag">Model Overview</span>}>
          <div className="panel-body">
            <div className="model-banner">
              <div className="icon-well">
                <BrainCircuit size={23} />
              </div>
              <div>
                <h3>ResNet50</h3>
                <p>Residual Convolutional Neural Network</p>
              </div>
            </div>
            <dl className="definition-list">
              <div>
                <dt>Architecture</dt>
                <dd>50-layer deep residual network</dd>
              </div>
              <div>
                <dt>Input dimensions</dt>
                <dd>224 × 224 × 3 (RGB)</dd>
              </div>
              <div>
                <dt>Learning approach</dt>
                <dd>Transfer learning & fine-tuning</dd>
              </div>
              <div>
                <dt>Overall accuracy</dt>
                <dd>98.09% on 1,518 test radiographs</dd>
              </div>
              <div>
                <dt>ROC-AUC score</dt>
                <dd>0.9980 multi-class discrimination</dd>
              </div>
            </dl>
            <Button asChild variant="link" size="sm" className="p-0 h-auto mt-5 text-[10px]">
              <Link to="/model-insights">
                View detailed model insights <ArrowRight />
              </Link>
            </Button>
          </div>
        </Panel>

        <Panel title="Explainable AI & interpretability" icon={Eye} action={<span className="tag">Visual Trust</span>}>
          <div className="panel-body prose">
            <div className="model-banner">
              <div className="icon-well">
                <Activity size={23} />
              </div>
              <div>
                <h3>Grad-CAM Visual Heatmaps</h3>
                <p>Gradient-weighted Class Activation Mapping</p>
              </div>
            </div>
            <p className="text-[11px] text-muted-foreground leading-relaxed">
              MediVision AI integrates Grad-CAM to make deep neural network attention transparent. Gradient signals from the final residual block (`conv5_block3_out`) reveal which pulmonary areas most strongly guided the predicted disease classification.
            </p>
            <div className="inline-note mt-3">
              <ShieldCheck size={15} />
              <p>Visual explanations facilitate scientific inspection and help detect model shortcut biases during screening.</p>
            </div>
            <Button asChild variant="link" size="sm" className="p-0 h-auto mt-4 text-[10px]">
              <Link to="/analyze">
                Launch an analysis to see Grad-CAM in action <ArrowRight />
              </Link>
            </Button>
          </div>
        </Panel>
      </div>

      <Disclaimer />
      <PageFooter />
    </motion.div>
  );
}
