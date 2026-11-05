// Dashed "- - - -" trail that follows the cursor and fades out.

// ===== SETTINGS =====
// Heart cursor on/off. Set to true to use the heart, false for the normal cursor.
const HEART_CURSOR = false;

// Dashed trail on/off. Set to true to show the trail, false to hide it.
const CURSOR_TRAIL = true;

if (HEART_CURSOR) document.documentElement.classList.add("heart-cursor");

(() => {
  if (!CURSOR_TRAIL) return;
  // Skip on touch screens and for people who prefer less motion
  if (!matchMedia("(pointer: fine)").matches) return;
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const COLOR = "205, 138, 138"; // rgb(205, 138, 138), same as the heart
  const LIFETIME = 500;        // ms before a bit of trail fully disappears
  const DASH = [7, 10];         // dash length, gap length (px)
  const WIDTH = 3;             // line thickness (px)

  const canvas = document.createElement("canvas");
  canvas.setAttribute("aria-hidden", "true");
  Object.assign(canvas.style, {
    position: "fixed", inset: "0", width: "100vw", height: "100vh",
    pointerEvents: "none", zIndex: "9999",
  });
  document.body.appendChild(canvas);
  const ctx = canvas.getContext("2d");

  function resize() {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = innerWidth * dpr;
    canvas.height = innerHeight * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  resize();
  addEventListener("resize", resize);

  let points = []; // {x, y, t, d} where d = distance travelled so far
  let travelled = 0;
  let running = false;

  addEventListener("mousemove", (e) => {
    const last = points[points.length - 1];
    if (last) travelled += Math.hypot(e.clientX - last.x, e.clientY - last.y);
    points.push({ x: e.clientX, y: e.clientY, t: performance.now(), d: travelled });
    if (!running) { running = true; requestAnimationFrame(draw); }
  });
  document.addEventListener("mouseleave", () => { points = []; });

  function draw(now) {
    points = points.filter((p) => now - p.t < LIFETIME);
    ctx.clearRect(0, 0, innerWidth, innerHeight);
    ctx.lineWidth = WIDTH;
    ctx.lineCap = "round";
    ctx.setLineDash(DASH);

    for (let i = 1; i < points.length; i++) {
      const a = points[i - 1], b = points[i];
      const alpha = 1 - (now - b.t) / LIFETIME; // older = fainter
      ctx.strokeStyle = `rgba(${COLOR}, ${alpha})`;
      ctx.lineDashOffset = -a.d; // keeps the dashes evenly spaced across segments
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    }

    if (points.length) requestAnimationFrame(draw);
    else { running = false; ctx.clearRect(0, 0, innerWidth, innerHeight); }
  }
})();
