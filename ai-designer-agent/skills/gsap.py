"""GSAP skill — professional JavaScript animation for standalone HTML designs."""

SKILL_DOCS = """
# GSAP MASTERY (for standalone HTML designs)

GSAP (GreenSock Animation Platform) is the gold standard for JavaScript animation.
Use it in all standalone HTML designs that need premium animation quality.

## CDN Setup (always include these in <head> or before </body>)
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/TextPlugin.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/SplitText.min.js"></script>

<script>
  gsap.registerPlugin(ScrollTrigger, TextPlugin);
</script>
```

## Core GSAP API

### 1. Basic tweens
```js
// gsap.to — from current state to target
gsap.to(".box", { x: 200, duration: 1, ease: "power3.out" });

// gsap.from — from these values to current state (entrance)
gsap.from(".hero-text", { opacity: 0, y: 60, duration: 0.8, ease: "power2.out" });

// gsap.fromTo — explicit start and end
gsap.fromTo(".card",
  { opacity: 0, y: 40, scale: 0.95 },
  { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "back.out(1.7)" }
);

// gsap.set — instant, no animation
gsap.set(".overlay", { opacity: 0, display: "none" });
```

### 2. Timelines — sequence and orchestrate
```js
const tl = gsap.timeline({ defaults: { ease: "power3.out", duration: 0.6 } });

tl.from(".nav", { y: -80, opacity: 0 })
  .from(".hero-badge", { scale: 0, opacity: 0, ease: "back.out(2)" }, "-=0.3")
  .from(".hero-title span", { opacity: 0, y: 80, stagger: 0.06, skewY: 3 }, "-=0.2")
  .from(".hero-subtitle", { opacity: 0, y: 20 }, "-=0.3")
  .from(".hero-cta", { opacity: 0, y: 20, stagger: 0.1 }, "-=0.2")
  .from(".hero-image", { opacity: 0, scale: 0.9, x: 40 }, "-=0.5");

// Timeline controls
tl.pause();
tl.play();
tl.reverse();
tl.seek(1.5); // jump to 1.5s
```

### 3. ScrollTrigger — scroll-linked animation (THE essential pattern)
```js
// Simple scroll reveal
gsap.from(".feature-card", {
  scrollTrigger: {
    trigger: ".feature-card",
    start: "top 85%",
    end: "bottom 20%",
    toggleActions: "play none none reverse",
  },
  opacity: 0,
  y: 60,
  duration: 0.7,
  stagger: 0.15,
  ease: "power2.out",
});

// Scrub — animation tied directly to scroll position
gsap.to(".hero-bg", {
  scrollTrigger: {
    trigger: ".hero",
    start: "top top",
    end: "bottom top",
    scrub: 1, // smooth scrubbing (1 = 1s lag)
  },
  y: -200,
  scale: 1.15,
});

// Pin a section while animating inside it
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".features-section",
    start: "top top",
    end: "+=300%",
    scrub: true,
    pin: true,
    anticipatePin: 1,
  },
});
tl.from(".feature-1", { opacity: 0, x: -100 })
  .from(".feature-2", { opacity: 0, x: 100 })
  .from(".feature-3", { opacity: 0, y: 100 });

// Batch — animate groups of elements on scroll
ScrollTrigger.batch(".card", {
  onEnter: (elements) => gsap.from(elements, {
    opacity: 0, y: 40, stagger: 0.1, duration: 0.6, ease: "power2.out",
  }),
});
```

### 4. Text animations — SplitText (when available) or manual
```js
// Manual character/word splitting
function splitIntoWords(element) {
  const text = element.textContent;
  element.innerHTML = text
    .split(" ")
    .map(w => `<span class="word" style="display:inline-block; overflow:hidden">
                 <span class="word-inner" style="display:inline-block">${w}</span>
               </span>`)
    .join(" ");
  return element.querySelectorAll(".word-inner");
}

const words = splitIntoWords(document.querySelector("h1"));
gsap.from(words, {
  scrollTrigger: { trigger: "h1", start: "top 80%" },
  y: "100%",
  opacity: 0,
  stagger: 0.05,
  duration: 0.7,
  ease: "power3.out",
});

// TextPlugin — typewriter
gsap.to(".typewriter", {
  text: { value: "Hello, World!", delimiter: "" },
  duration: 2,
  ease: "none",
});
```

### 5. Parallax layers
```js
const layers = [
  { el: ".parallax-bg", speed: 0.3 },
  { el: ".parallax-mid", speed: 0.6 },
  { el: ".parallax-fg", speed: 0.9 },
];

layers.forEach(({ el, speed }) => {
  gsap.to(el, {
    scrollTrigger: {
      trigger: "body",
      start: "top top",
      end: "bottom bottom",
      scrub: true,
    },
    y: () => -(ScrollTrigger.maxScroll(window) * speed),
    ease: "none",
  });
});
```

### 6. Cursor effects
```js
const cursor = document.querySelector(".cursor");
const cursorInner = document.querySelector(".cursor-inner");

let mouseX = 0, mouseY = 0;
let curX = 0, curY = 0;

document.addEventListener("mousemove", (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
  gsap.to(cursorInner, { x: mouseX - 4, y: mouseY - 4, duration: 0.1 });
});

gsap.ticker.add(() => {
  curX += (mouseX - curX) * 0.12;
  curY += (mouseY - curY) * 0.12;
  gsap.set(cursor, { x: curX - 20, y: curY - 20 });
});

// Hover states
document.querySelectorAll("a, button").forEach(el => {
  el.addEventListener("mouseenter", () => {
    gsap.to(cursor, { scale: 2.5, duration: 0.3, ease: "power2.out" });
    gsap.to(cursorInner, { scale: 0, duration: 0.2 });
  });
  el.addEventListener("mouseleave", () => {
    gsap.to(cursor, { scale: 1, duration: 0.4, ease: "elastic.out(1, 0.5)" });
    gsap.to(cursorInner, { scale: 1, duration: 0.2 });
  });
});
```

### 7. Page loader with reveal
```js
const loader = document.querySelector(".loader");
const progress = document.querySelector(".loader-progress");

const tl = gsap.timeline();
tl.to(progress, { width: "100%", duration: 1.5, ease: "power2.inOut" })
  .to(loader, { yPercent: -100, duration: 0.8, ease: "power3.inOut" }, "+=0.2")
  .from(".page-content", { opacity: 0, y: 30, duration: 0.6, ease: "power2.out" }, "-=0.3");
```

### 8. Magnetic button
```js
document.querySelectorAll(".btn-magnetic").forEach(btn => {
  btn.addEventListener("mousemove", (e) => {
    const rect = btn.getBoundingClientRect();
    const x = (e.clientX - rect.left - rect.width / 2) * 0.35;
    const y = (e.clientY - rect.top - rect.height / 2) * 0.35;
    gsap.to(btn, { x, y, duration: 0.3, ease: "power2.out" });
  });
  btn.addEventListener("mouseleave", () => {
    gsap.to(btn, { x: 0, y: 0, duration: 0.6, ease: "elastic.out(1, 0.5)" });
  });
});
```

### 9. Counter animation
```js
function animateCounter(el, target, duration = 2) {
  const obj = { value: 0 };
  gsap.to(obj, {
    value: target,
    duration,
    ease: "power2.out",
    onUpdate: () => {
      el.textContent = Math.round(obj.value).toLocaleString();
    },
    scrollTrigger: { trigger: el, start: "top 80%" },
  });
}

document.querySelectorAll("[data-count]").forEach(el => {
  animateCounter(el, parseInt(el.dataset.count));
});
```

### 10. Easings cheat-sheet
```
power1-4.out   — standard decelerations (power3.out is the workhorse)
back.out(1.7)  — slight overshoot, great for entrances
elastic.out(1, 0.5) — springy, use sparingly
expo.out       — fast settle, premium feel
circ.out       — circular, dramatic
slow(0.7,0.7,false) — slowmo effect for dramatic reveals
CustomEase.create("myEase", "M0,0 C0.126,0.382 0.282,0.674 0.44,0.822...") — bezier
```

## Anti-patterns to AVOID
- Never animate `width`, `height`, `top`, `left`, `margin` — use `transform` (x, y, scale)
- Don't create ScrollTriggers inside scroll handlers
- Always call `ScrollTrigger.refresh()` after layout changes
- Kill animations on component unmount: `ctx.revert()` or `tl.kill()`
"""
