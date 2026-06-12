/* Event-Den — shared interactions (no dependencies) */
(function () {
  "use strict";

  /* Mobile nav */
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* Hero crossfade slider */
  var slides = document.querySelectorAll(".hero-slide");
  if (slides.length > 1 && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var i = 0;
    setInterval(function () {
      slides[i].classList.remove("active");
      i = (i + 1) % slides.length;
      slides[i].classList.add("active");
    }, 6000);
  }

  /* Scroll reveal */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* Gallery lightbox */
  var galleryImgs = document.querySelectorAll(".gallery-grid img");
  if (galleryImgs.length) {
    var lb = document.createElement("div");
    lb.className = "lightbox";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-label", "Enlarged gallery image");
    lb.innerHTML = '<button type="button" aria-label="Close image">✕</button><img alt="">';
    document.body.appendChild(lb);
    var lbImg = lb.querySelector("img");
    var close = function () { lb.classList.remove("open"); };
    lb.querySelector("button").addEventListener("click", close);
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
    galleryImgs.forEach(function (img) {
      img.setAttribute("tabindex", "0");
      var open = function () {
        lbImg.src = img.src.replace(/w=\d+/, "w=1600");
        lbImg.alt = img.alt;
        lb.classList.add("open");
      };
      img.addEventListener("click", open);
      img.addEventListener("keydown", function (e) { if (e.key === "Enter") open(); });
    });
  }

  /* Current-year stamp */
  var yr = document.querySelector("[data-year]");
  if (yr) { yr.textContent = new Date().getFullYear(); }
})();

/* Champagne hero — faded closed-bottle photo transitions to popped bottle as the mouse moves; confetti at full pop */
(function () {
  "use strict";
  var stage = document.getElementById("champagne");
  var canvas = document.getElementById("confetti-canvas");
  if (!stage || !canvas) return;

  var closed = stage.querySelector(".bottle-closed");
  var open = stage.querySelector(".bottle-open");
  var hint = stage.querySelector(".champagne-hint");
  var hero = canvas.parentElement;
  var ctx = canvas.getContext("2d");
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var COLORS = ["#c9a14e", "#e0c285", "#7a4fb0", "#a98ad1", "#f3ecdf"];
  var particles = [], energy = 0, popped = false, lastX = null, lastY = null, raf = null;
  var MAX = 900;

  function size() { canvas.width = hero.clientWidth; canvas.height = hero.clientHeight; }
  size();
  window.addEventListener("resize", size);

  function setProgress(t) {
    closed.style.opacity = (0.34 * (1 - t)).toFixed(3);
    open.style.opacity = (0.62 * t).toFixed(3);
  }

  function burst() {
    if (popped) return;
    popped = true;
    stage.classList.add("popped");
    closed.style.opacity = ""; open.style.opacity = "";
    if (hint) hint.textContent = "cheers!";
    var ox = canvas.width * 0.78, oy = canvas.height * 0.35;
    var n = reduced ? 40 : 170;
    for (var i = 0; i < n; i++) {
      var a = -Math.PI / 2 + (Math.random() - 0.5) * 1.7;
      var sp = 6 + Math.random() * 14;
      particles.push({
        x: ox, y: oy, vx: Math.cos(a) * sp - 2, vy: Math.sin(a) * sp,
        g: 0.22 + Math.random() * 0.1, rot: Math.random() * Math.PI, vr: (Math.random() - 0.5) * 0.3,
        w: 5 + Math.random() * 7, h: 3 + Math.random() * 5,
        life: 1, decay: 0.004 + Math.random() * 0.006,
        c: COLORS[(Math.random() * COLORS.length) | 0], round: Math.random() < 0.3
      });
    }
    if (!raf) loop();
    setTimeout(reset, 8000);
  }

  function reset() {
    popped = false; energy = 0;
    stage.classList.remove("popped");
    setProgress(0);
    if (hint) hint.textContent = "move your mouse \u00b7 pop the bottle";
  }

  function loop() {
    raf = requestAnimationFrame(loop);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles = particles.filter(function (p) { return p.life > 0 && p.y < canvas.height + 40; });
    if (!particles.length) { cancelAnimationFrame(raf); raf = null; return; }
    particles.forEach(function (p) {
      p.vy += p.g; p.vx *= 0.99; p.x += p.vx; p.y += p.vy;
      p.rot += p.vr; p.life -= p.decay;
      ctx.save(); ctx.globalAlpha = Math.max(p.life, 0);
      ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.fillStyle = p.c;
      if (p.round) { ctx.beginPath(); ctx.arc(0, 0, p.w / 2, 0, 7); ctx.fill(); }
      else ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
      ctx.restore();
    });
  }

  if (!reduced) {
    hero.addEventListener("mousemove", function (e) {
      if (popped) return;
      if (lastX !== null) {
        energy = Math.min(energy + Math.min(Math.abs(e.clientX - lastX) + Math.abs(e.clientY - lastY), 40), MAX);
        setProgress(energy / MAX);
        if (energy >= MAX) burst();
      }
      lastX = e.clientX; lastY = e.clientY;
    });
  }
  /* Tap anywhere on the hero pops it (mobile + reduced motion + accessibility) */
  hero.addEventListener("click", function () { if (!popped) burst(); });
})();
