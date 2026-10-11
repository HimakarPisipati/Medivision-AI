export const MAX_IMAGE_BYTES = 20 * 1024 * 1024;
export function validateImage(file: File): string | undefined {
  if (!['image/png', 'image/jpeg'].includes(file.type) || !/\.(png|jpe?g)$/i.test(file.name)) return 'Please choose a PNG, JPG, or JPEG image.';
  if (!file.size) return 'This file is empty. Please choose another image.';
  if (file.size > MAX_IMAGE_BYTES) return 'Please choose an image smaller than 20 MB.';
  return undefined;
}
export function readImage(file: File): Promise<{ url: string; width: number; height: number }> {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file); const image = new Image();
    image.onload = () => resolve({ url, width: image.naturalWidth, height: image.naturalHeight });
    image.onerror = () => { URL.revokeObjectURL(url); reject(new Error('This image could not be opened. It may be corrupted. Please choose another file.')); };
    image.src = url;
  });
}
