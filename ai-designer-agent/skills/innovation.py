"""Innovation skill — novel interactions, award-winning techniques, creative direction."""

SKILL_DOCS = """
# INNOVATION MANDATE — Beyond the Obvious

You are not here to produce generic templates. Every design must include at least one
thing the user won't have seen before, or at least one interaction that makes them say
"I didn't know CSS/JS could do that."

## Creative Direction Patterns

### 1. The "Unexpected Delight" principle
Before building: identify the one thing everyone expects, then reject it.
- Hero with image grid? → Use a 3D perspective tilt that follows the cursor.
- Standard card hover? → Cards breathe slowly when idle, then snap to attention on hover.
- Pricing table? → The selected plan physically lifts off the page, others recede.
- Loading state? → A generative art piece that resolves into the content.

### 2. Interaction patterns worth stealing from award sites

**Cursor takeover**
```js
// The cursor morphs into context-aware shapes
const states = {
  default: { width: 12, height: 12, borderRadius: "50%" },
  link: { width: 48, height: 48, borderRadius: "50%", mixBlendMode: "difference" },
  video: { width: 80, height: 80, borderRadius: "50%", content: "▶" },
  drag: { width: 60, height: 60, borderRadius: "8px", rotate: "45deg" },
};
```

**Sticky text distortion on scroll**
```css
/* Horizontal scroll sections that feel like film strips */
.film-strip {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
}
.film-frame {
  flex: 0 0 100vw;
  scroll-snap-align: center;
  height: 100svh;
}
```

**Text that reacts to mouse position**
```js
document.querySelectorAll(".reactive-text").forEach(el => {
  el.addEventListener("mousemove", (e) => {
    const { left, top, width, height } = el.getBoundingClientRect();
    const x = (e.clientX - left - width / 2) / width;
    const y = (e.clientY - top - height / 2) / height;
    el.style.transform = `perspective(600px) rotateY(${x * 10}deg) rotateX(${-y * 10}deg)`;
  });
  el.addEventListener("mouseleave", () => {
    el.style.transform = "";
    el.style.transition = "transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)";
  });
});
```

### 3. Navigation innovations

**Drawer with spring physics**
```css
.nav-drawer {
  transform: translateX(-100%);
  transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.nav-drawer.open {
  transform: translateX(0);
}
```

**Mega menu with staggered grid entrance**
Menus animate in column by column, not all at once.

**Navigation that breathes with content**
Nav background becomes increasingly opaque as user scrolls, matching the page's dominant color using `document.elementFromPoint()`.

**Full-screen overlay nav**
The entire viewport transforms into the menu with a morph transition.

### 4. Hero section innovations

**Kinetic typography** — Each letter has its own velocity:
```js
letters.forEach((letter, i) => {
  gsap.from(letter, {
    y: () => gsap.utils.random(-200, -50),
    x: () => gsap.utils.random(-100, 100),
    rotation: () => gsap.utils.random(-90, 90),
    opacity: 0,
    duration: gsap.utils.random(0.6, 1.2),
    ease: "power3.out",
    delay: i * 0.03,
  });
});
```

**3D card grid hero**
```css
.hero-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  perspective: 1000px;
  transform-style: preserve-3d;
}
.hero-card:nth-child(odd) { transform: translateZ(30px); }
.hero-card:nth-child(even) { transform: translateZ(-10px) rotateX(5deg); }
```

**Gradient text with animated background**
```css
.hero-title {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #667eea 100%);
  background-size: 300% 300%;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradient-shift 6s ease infinite;
}
@keyframes gradient-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
```

### 5. Scroll storytelling patterns

**Morphing SVG on scroll**
```js
const paths = ["M 0 0 L 100 0 L 100 100 L 0 100", "M 10 10 L 90 5 L 95 90 L 5 95"];
ScrollTrigger.create({
  trigger: ".morph-section",
  scrub: true,
  onUpdate: (self) => {
    const progress = self.progress;
    svgPath.setAttribute("d", interpolatePath(paths[0], paths[1], progress));
  },
});
```

**Horizontal scroll with zoom-in on stop**
```js
const sections = gsap.utils.toArray(".panel");
gsap.to(sections, {
  xPercent: -100 * (sections.length - 1),
  ease: "none",
  scrollTrigger: {
    trigger: ".container",
    pin: true,
    scrub: 1,
    snap: 1 / (sections.length - 1),
    end: () => "+=" + document.querySelector(".container").offsetWidth,
  },
});
```

**Timeline scrubbing** — content appears as you scroll through a visual timeline.

### 6. Card & content innovations

**Tilt card with inner parallax layers**
```js
function initTiltCard(card) {
  const layers = card.querySelectorAll("[data-depth]");

  card.addEventListener("mousemove", (e) => {
    const { left, top, width, height } = card.getBoundingClientRect();
    const x = (e.clientX - left - width / 2) / (width / 2);
    const y = (e.clientY - top - height / 2) / (height / 2);

    card.style.transform = `perspective(1000px) rotateY(${x * 8}deg) rotateX(${-y * 8}deg)`;

    layers.forEach(layer => {
      const depth = parseFloat(layer.dataset.depth);
      layer.style.transform = `translateX(${x * depth * 20}px) translateY(${y * depth * 20}px)`;
    });
  });
}
```

**Cards that reveal content on hover via clip-path**
```css
.card-reveal__content {
  clip-path: inset(0 0 100% 0);
  transition: clip-path 0.4s cubic-bezier(0.77, 0, 0.175, 1);
}
.card:hover .card-reveal__content {
  clip-path: inset(0 0 0 0);
}
```

**Infinite marquee** — trusted logos, testimonials, features
```css
.marquee {
  display: flex;
  overflow: hidden;
  gap: 2rem;
}
.marquee__track {
  display: flex;
  gap: 2rem;
  animation: marquee 20s linear infinite;
  flex-shrink: 0;
  min-width: 100%;
}
.marquee:hover .marquee__track {
  animation-play-state: paused;
}
@keyframes marquee {
  from { transform: translateX(0); }
  to { transform: translateX(-100%); }
}
```

### 7. Forms that feel alive

**Floating label with color transition** — label moves AND the border traces around the input.
**Shake animation on invalid** — `animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both`
**Progress stepper** — multi-step form where each step slides in and previous slides out.
**Real-time validation** — green checkmark / red cross animates into existence as user types.

### 8. Data visualization moments

**Animated bar chart on scroll**:
```js
bars.forEach((bar, i) => {
  gsap.from(bar, {
    scaleY: 0,
    transformOrigin: "bottom",
    duration: 0.8,
    delay: i * 0.1,
    ease: "power3.out",
    scrollTrigger: { trigger: bar, start: "top 80%" },
  });
});
```

**Number countups** with easing — metrics that count to their value as they enter view.
**Ring/donut charts** that draw themselves with SVG stroke-dashoffset animation.

### 9. Dark luxury patterns

**Auroral background** — slowly shifting mesh gradient simulating northern lights:
```css
.aurora {
  background:
    radial-gradient(ellipse 60% 40% at 30% 50%, oklch(55% 0.3 290 / 0.6), transparent),
    radial-gradient(ellipse 80% 60% at 70% 30%, oklch(65% 0.25 200 / 0.4), transparent),
    oklch(8% 0.015 260);
  animation: aurora-shift 12s ease-in-out infinite alternate;
}
@keyframes aurora-shift {
  from { background-position: 0% 50%, 100% 50%; }
  to { background-position: 100% 50%, 0% 50%; }
}
```

**Foil/holographic effect on hover**:
```css
.holographic {
  background: linear-gradient(135deg,
    oklch(75% 0.3 0 / 0.8) 0%,
    oklch(75% 0.3 60 / 0.8) 20%,
    oklch(75% 0.3 120 / 0.8) 40%,
    oklch(75% 0.3 200 / 0.8) 60%,
    oklch(75% 0.3 280 / 0.8) 80%,
    oklch(75% 0.3 340 / 0.8) 100%
  );
  background-size: 200% 200%;
  background-clip: text;
  -webkit-background-clip: text;
  transition: background-position 0.3s ease;
}
.holographic:hover {
  background-position: 100% 100%;
}
```

### 10. Mobile-first innovations

**Bottom sheet pattern** — content slides up from bottom, feels native:
```css
.bottom-sheet {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  transform: translateY(100%);
  border-radius: 24px 24px 0 0;
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  touch-action: pan-y;
}
.bottom-sheet.open {
  transform: translateY(0);
}
```

**Haptic-like feedback** — `navigator.vibrate(10)` on key interactions (mobile).
**Swipe-to-action** — drag cards to reveal actions beneath.

## The Innovation Checklist

Before finalizing any design, ask:
□ Does this feel like something the user has seen before?
□ Is there one interaction that will make them say "oh, that's clever"?
□ Does the animation tell a story, or is it just decoration?
□ Have I used at least one cutting-edge CSS feature (oklch, container queries, scroll-driven)?
□ Is there a micro-interaction that rewards careful attention?
□ Does the design feel like it belongs in an Awwwards showcase?

If you answer "no" to any of these, keep iterating.
"""
