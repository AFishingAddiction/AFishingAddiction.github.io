// Re-encodes referenced images over a size threshold as WebP.
// Usage: node optimize-images.mjs <repo-root> <refs-file> [--dry]
// refs-file: one /assets/img/... path per line (images referenced by the site).
// Requires the "sharp" package (install it outside the repo and set NODE_PATH).
// - existing .webp: re-encoded in place at the same dimensions (max width 1600)
// - .jpg/.jpeg/.png: written as a sibling .webp (max width 1600), originals kept
// Prints a JSON map of converted paths so references can be rewritten.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const sharp = require('sharp');

const root = path.resolve(process.argv[2] || '.');
const dry = process.argv.includes('--dry');
const THRESHOLD = 120 * 1024;
const MAX_WIDTH = 1600;
const QUALITY = 75;

const refs = fs.readFileSync(path.resolve(process.argv[3]), 'utf8')
  .split(/\r?\n/).filter(Boolean);

const converted = {};
let before = 0;
let after = 0;

for (const ref of refs) {
  const file = path.join(root, decodeURI(ref));
  if (!fs.existsSync(file)) continue;
  const size = fs.statSync(file).size;
  if (size < THRESHOLD) continue;
  const ext = path.extname(file).toLowerCase();
  const out = ext === '.webp' ? file : file.slice(0, -ext.length) + '.webp';
  const buf = await sharp(fs.readFileSync(file)).rotate()
    .resize({ width: MAX_WIDTH, withoutEnlargement: true })
    .webp({ quality: QUALITY, effort: 5 })
    .toBuffer();
  if (ext === '.webp' && buf.length >= size) continue;
  before += size;
  after += buf.length;
  if (!dry) fs.writeFileSync(out, buf);
  if (ext !== '.webp') converted[ref] = ref.slice(0, -ext.length) + '.webp';
  console.error(`${(size / 1024) | 0}KB -> ${(buf.length / 1024) | 0}KB  ${ref}`);
}
console.error(`TOTAL ${(before / 1024 / 1024).toFixed(1)}MB -> ${(after / 1024 / 1024).toFixed(1)}MB`);
console.log(JSON.stringify(converted, null, 1));
