// usage: node render.js preview 1.5 4 9 ...   -> stills/t_<sec>.png
//        node render.js full                   -> video_silent.mp4
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const FFMPEG = process.env.FFMPEG;
const FPS = 30, FRAMES = 900;
const root = __dirname;
const types = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.woff2': 'font/woff2', '.png': 'image/png' };

const server = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  fs.readFile(p, (err, data) => {
    if (err) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream' });
    res.end(data);
  });
});

(async () => {
  await new Promise(r => server.listen(8765, r));
  const browser = await chromium.launch({ args: ['--no-proxy-server'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('console', m => console.log('[page]', m.text()));
  page.on('pageerror', e => console.log('[pageerror]', e.message));
  await page.goto('http://127.0.0.1:8765/promo.html');
  const dots = await page.evaluate(() => window.ready);
  console.log('land dots', dots);
  const canvas = await page.$('#c');
  const grab = async f => {
    await page.evaluate(f => window.renderAt(f), f);
    return canvas.screenshot({ type: 'png' });
  };

  const mode = process.argv[2];
  if (mode === 'preview') {
    fs.mkdirSync(path.join(root, 'stills'), { recursive: true });
    for (const s of process.argv.slice(3)) {
      fs.writeFileSync(path.join(root, 'stills', `t_${s}.png`), await grab(Math.round(parseFloat(s) * FPS)));
    }
  } else {
    const ff = spawn(FFMPEG, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
      path.join(root, 'video_silent.mp4')], { stdio: ['pipe', 'ignore', 'inherit'] });
    const t0 = Date.now();
    for (let f = 0; f < FRAMES; f++) {
      const buf = await grab(f);
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (f % 90 === 0) console.log(`frame ${f}/${FRAMES} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
  }
  await browser.close();
  server.close();
})();
