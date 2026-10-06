// Full-page capture at an exact viewport (headless Chrome clamps windows below 500px wide).
// node cdp-capture.mjs <out.png> <width> <height> <url> [mobile]
import { spawn } from "node:child_process";
import { writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [out, w, h, url, mobile] = process.argv.slice(2);
const chrome = spawn("C:/Program Files/Google/Chrome/Application/chrome.exe", [
  "--headless=new", "--disable-gpu", "--hide-scrollbars", "--remote-debugging-port=9333",
  `--user-data-dir=${mkdtempSync(join(tmpdir(), "tp-cdp-"))}`, "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let target;
for (let i = 0; i < 50 && !target; i++) {
  try { target = (await (await fetch("http://127.0.0.1:9333/json/list")).json()).find((t) => t.type === "page"); } catch { await sleep(200); }
}
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let id = 0;
const pending = new Map();
ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise((r) => { pending.set(++id, r); ws.send(JSON.stringify({ id, method, params })); });

await send("Emulation.setDeviceMetricsOverride", { width: +w, height: +h, deviceScaleFactor: 1, mobile: mobile === "mobile" });
await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
await send("Page.enable");
await send("Page.navigate", { url });
await sleep(6000);
const { cssContentSize } = await send("Page.getLayoutMetrics");
const shot = await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true,
  clip: { x: 0, y: 0, width: +w, height: Math.ceil(cssContentSize.height), scale: 1 } });
writeFileSync(out, Buffer.from(shot.data, "base64"));
const { result } = await send("Runtime.evaluate", { expression: "document.documentElement.scrollWidth" });
console.log(`${out}: ${w}x${Math.ceil(cssContentSize.height)}, scrollWidth ${result.value}`);
ws.close();
chrome.kill();
process.exit(0);
