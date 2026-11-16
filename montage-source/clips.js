const { chromium } = require('playwright');
const { spawnSync, spawn } = require('child_process');
const path = require('path');
const FPS = 30;
(async () => {
  const browser = await chromium.launch();
  // intro / outro clips from ad.html scenes
  for (const [name, id, off, dur] of [['intro', 's2', 3400, 3.0], ['outro', 's5', 21300, 4.5]]) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
    await page.goto('file://' + path.join(__dirname, 'ad.html'));
    await page.evaluate(() => document.fonts.ready);
    await page.addStyleTag({ content: `.scene:not(#${id}){display:none!important}` });
    await page.waitForTimeout(300);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', `assets/${name}.mp4`], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < dur * FPS; i++) {
      await page.evaluate((t) => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = t; }), off + i * 1000 / FPS);
      const b = await page.screenshot({ type: 'jpeg', quality: 97 });
      if (!ff.stdin.write(b)) await new Promise((r) => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise((r) => ff.on('close', r)); await page.close();
  }
  // transparent overlays
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(__dirname, 'labels.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const n = await page.evaluate(() => document.querySelectorAll('.o').length);
  for (let i = 0; i < n; i++) {
    await page.evaluate((i) => document.querySelectorAll('.o').forEach((e, j) => e.style.display = j === i ? 'flex' : 'none'), i);
    await page.screenshot({ path: `assets/o${i}.png`, omitBackground: true });
  }
  await browser.close();
})();
