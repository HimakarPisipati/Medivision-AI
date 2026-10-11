import { describe, it, expect } from 'vitest';
import { CLASSES } from '@/types/api';
import { adaptPrediction, validProbability } from '@/services/predictionService';
import { validateImage, MAX_IMAGE_BYTES } from '@/lib/upload';
describe('Scientific output rules', () => {
  it('keeps the exact model class order', () => { expect([...CLASSES]).toEqual(['COVID','Normal','Viral Pneumonia']); });
  it('does not recompute the backend prediction', () => { const output = adaptPrediction({ predicted_class: 'COVID', probabilities: { COVID: 0.1, Normal: 0.8, 'Viral Pneumonia': 0.1 } }); expect(output.predicted_class).toBe('COVID'); expect(output.probabilities.Normal).toBe(0.8); });
  it('does not invent missing probabilities or confidence', () => { const output = adaptPrediction({ predicted_class: 'Normal' }); expect(output.probabilities).toEqual({}); expect(output.confidence).toBeUndefined(); });
  it('does not format invalid probability values', () => { const output = adaptPrediction({ predicted_class: 'COVID', confidence: 97, probabilities: { COVID: 97, Normal: -1, 'Viral Pneumonia': '0.1' } }); expect(output.confidence).toBeUndefined(); expect(output.probabilities).toEqual({}); expect(validProbability(NaN)).toBe(false); });
  it('rejects unsupported classes', () => { expect(() => adaptPrediction({ predicted_class: 'Other' })).toThrow('not supported'); });
  it('does not invent a confidence caution threshold', () => { expect(adaptPrediction({ predicted_class: 'Normal', confidence: 0.1 }).caution).toBeUndefined(); });
  it('accepts only an explicitly defined caution with semantics', () => { const output = adaptPrediction({ predicted_class: 'Normal', caution: { threshold: 0.4, message: 'Project-configured review flag' } }); expect(output.caution).toEqual({ threshold: 0.4, message: 'Project-configured review flag' }); });
  it('does not fabricate Grad-CAM images', () => { const result = adaptPrediction({ predicted_class: 'Normal' }); expect(result.gradcam?.heatmap_url).toBeUndefined(); expect(result.gradcam?.overlay_url).toBeUndefined(); });
});
describe('Upload validation', () => {
  it('accepts PNG and JPEG uploads', () => { for (const [name,type] of ([['xray.png','image/png'],['xray.jpg','image/jpeg'],['xray.jpeg','image/jpeg']] as const)) expect(validateImage(new File(['data'], name, { type }))).toBeUndefined(); });
  it('rejects unsupported formats', () => { expect(validateImage(new File(['data'], 'scan.gif', { type: 'image/gif' }))).toContain('PNG'); });
  it('rejects empty uploads', () => { expect(validateImage(new File([], 'scan.png', { type: 'image/png' }))).toContain('empty'); });
  it('enforces the documented frontend safety limit', () => { const large = new File(['data'], 'scan.png', { type: 'image/png' }); Object.defineProperty(large, 'size', { value: MAX_IMAGE_BYTES + 1 }); expect(validateImage(large)).toContain('20 MB'); });
});
