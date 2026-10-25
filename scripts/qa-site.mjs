// 系统Chrome独立配置，只访问构建网站，结束后关闭浏览器及本机服务。
import { chromium } from 'playwright-core';
import { createServer } from 'node:http';
import { readFile, mkdir, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const site = path.join(root, 'work/site');
const output = path.join(root, 'work/qa-site');
await mkdir(output, { recursive: true });
const report = { gates: [], consoleErrors: [], pageErrors: [], screenshots: [] };
const server = createServer(async (request, response) => {
  try {
    const pathname = new URL(request.url, 'http://127.0.0.1').pathname;
    if (!pathname.startsWith('/zhao-picks/')) { response.writeHead(404); response.end(); return; }
    let target = path.resolve(site, decodeURIComponent(pathname.slice('/zhao-picks/'.length)));
    if (target !== site && !target.startsWith(site + path.sep)) throw new Error('outside root');
    if ((await stat(target)).isDirectory()) target = path.join(target, 'index.html');
    const data = await readFile(target);
    const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2' };
    response.writeHead(200, { 'Content-Type': types[path.extname(target)] || 'application/octet-stream' });
    response.end(data);
  } catch { response.writeHead(404); response.end('not found'); }
});
let browser;
try {
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(18431, '127.0.0.1', resolve); });
  browser = await chromium.launch({ channel: 'chrome', headless: true });
  const context = await browser.newContext({ locale: 'zh-CN', viewport: { width: 1280, height: 900 } });
  const page = await context.newPage();
  page.setDefaultTimeout(15000);
  page.on('pageerror', error => report.pageErrors.push(error.message));
  page.on('console', message => { if (message.type() === 'error') report.consoleErrors.push(message.text()); });
  const home = 'http://127.0.0.1:18431/zhao-picks/';
  await page.goto(home, { waitUntil: 'networkidle', timeout: 20000 });
  await page.locator('main h1').waitFor();
  assert.match(await page.locator('main').innerText(), /我的开源精选/);
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
  await page.screenshot({ path: path.join(output, 'desktop-home.png') });
  report.screenshots.push('desktop-home.png');
  await page.locator('main a[href="/zhao-picks/reviews/stretchly/"]').click();
  await page.waitForURL('**/reviews/stretchly/');
  assert.match(await page.locator('main h1').innerText(), /Stretchly/);
  await page.screenshot({ path: path.join(output, 'desktop-detail.png') });
  report.screenshots.push('desktop-detail.png');
  await page.locator('.page-context a').first().click();
  await page.waitForURL(home);
  report.gates.push('G2 首页→独立详情→首页实际点击通过');
  const search = page.getByRole('searchbox', { name: '搜索项目、用途或关键词' });
  await search.fill('生词');
  const results = page.locator('#picks-search-results');
  await results.getByRole('link', { name: /AI Vocabulary Builder/ }).click();
  await page.waitForURL('**/reviews/ai-vocabulary-builder/');
  await search.fill('Stretchly');
  await results.getByRole('link', { name: /Stretchly/ }).waitFor();
  await search.fill('不存在的项目测试关键词');
  await results.getByRole('status').filter({ hasText: '没有找到' }).waitFor();
  await search.press('Escape');
  assert.equal(await results.isVisible(), false);
  report.gates.push('G3 中文/英文搜索、结果跳转、空结果与Escape关闭通过');
  await page.goto(home + '404.html', { waitUntil: 'networkidle' });
  await page.locator('main a').filter({ hasText: '返回精选首页' }).click();
  await page.waitForURL(home);
  await page.setViewportSize({ width: 390, height: 844 });
  await page.reload({ waitUntil: 'networkidle' });
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
  assert.equal(await search.isVisible(), true);
  assert.equal(await page.locator('main .picks-directory').first().evaluate(table => getComputedStyle(table).display), 'block');
  await page.screenshot({ path: path.join(output, 'mobile-home.png') });
  report.screenshots.push('mobile-home.png');
  const toggle = page.locator('#menu-button');
  await toggle.click();
  const nav = page.locator('#site-nav');
  await nav.getByRole('link', { name: '项目目录', exact: true }).click();
  await page.waitForURL('**/projects/');
  await page.locator('main a[href="/zhao-picks/reviews/bibigpt-v1/"]').click();
  await page.waitForURL('**/reviews/bibigpt-v1/');
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
  await page.screenshot({ path: path.join(output, 'mobile-detail.png') });
  report.screenshots.push('mobile-detail.png');
  report.gates.push('G3 404返回、390手机导航/详情、无横向溢出通过');
  assert.deepEqual(report.pageErrors, []);
  assert.deepEqual(report.consoleErrors, []);
  report.status = 'passed';
  report.browser = browser.version();
  console.log(JSON.stringify(report));
} catch (error) {
  report.status = 'failed'; report.error = String(error); console.error(error); process.exitCode = 1;
} finally {
  await browser?.close();
  await new Promise(resolve => server.close(resolve));
  await writeFile(path.join(output, 'report.json'), JSON.stringify(report, null, 2));
}
