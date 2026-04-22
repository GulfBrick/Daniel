"""Advanced CSS skill — cutting-edge CSS techniques for super HiFi designs."""

SKILL_DOCS = """
# ADVANCED CSS MASTERY — Super HiFi Techniques

## 1. oklch Color System (perceptually uniform, vivid, modern)
```css
:root {
  /* oklch(lightness chroma hue) — more vivid and predictable than HSL */
  --color-primary: oklch(65% 0.25 260);      /* vivid purple-blue */
  --color-primary-light: oklch(75% 0.2 260);
  --color-primary-dark: oklch(45% 0.3 260);
  --color-accent: oklch(72% 0.28 160);       /* vibrant teal */
  --color-danger: oklch(62% 0.25 25);        /* rich red */
  --color-surface: oklch(98% 0.005 260);     /* near-white with blue tint */
  --color-bg: oklch(12% 0.02 260);           /* near-black with depth */
  --color-text: oklch(20% 0.01 260);

  /* P3 wide gamut with oklch fallback */
  --color-hero-glow: color(display-p3 0.4 0.1 1);
}

/* Dynamic color with color-mix */
.card-hover {
  background: color-mix(in oklch, var(--color-primary) 15%, white);
}
```

## 2. Variable Fonts — dynamic typography
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

:root {
  --font-weight-base: 400;
  --font-optical-size: 16;
}

/* Fluid type with clamp() */
h1 {
  font-size: clamp(2.5rem, 5vw + 1rem, 6rem);
  font-weight: 800;
  font-variation-settings: "wght" 800, "opsz" 48;
  line-height: 1.05;
  letter-spacing: -0.03em;
}

/* Animated weight on hover */
.nav-link {
  font-variation-settings: "wght" 400;
  transition: font-variation-settings 0.2s ease;
}
.nav-link:hover {
  font-variation-settings: "wght" 700;
}
```

## 3. CSS Scroll-Driven Animations (no JavaScript needed)
```css
@keyframes reveal-up {
  from { opacity: 0; translate: 0 40px; }
  to { opacity: 1; translate: 0 0; }
}

/* Animate when element enters viewport */
.card {
  animation: reveal-up linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 30%;
}

/* Progress bar tied to page scroll */
.progress-bar {
  animation: grow-x linear;
  animation-timeline: scroll();
  transform-origin: left;
}
@keyframes grow-x {
  from { scaleX: 0; }
  to { scaleX: 1; }
}

/* Parallax with scroll() */
.hero-bg {
  animation: parallax linear;
  animation-timeline: scroll(root);
  animation-range: 0% 50%;
}
@keyframes parallax {
  to { translate: 0 -30%; }
}
```

## 4. Container Queries — truly responsive components
```css
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 480px) {
  .card {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
  .card__image { aspect-ratio: 1; }
}

@container card (max-width: 280px) {
  .card__actions { flex-direction: column; }
}
```

## 5. CSS Grid Mastery — advanced layouts
```css
/* Subgrid — align nested elements to parent grid */
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
}
.gallery-item {
  display: grid;
  grid-row: span 2;
  grid-template-rows: subgrid; /* child rows align to parent! */
}

/* Asymmetric editorial layout */
.editorial {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  grid-template-rows: repeat(4, auto);
}
.editorial__feature {
  grid-column: 2 / 4;
  grid-row: 1 / 3;
}
.editorial__sidebar {
  grid-column: 1 / 2;
  grid-row: 1 / 4;
  writing-mode: vertical-rl;
}

/* Masonry (Chrome 2024+) */
.masonry {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: masonry;
  gap: 1.5rem;
}
```

## 6. Advanced Glassmorphism
```css
.glass-card {
  background: oklch(100% 0 0 / 0.08);
  backdrop-filter: blur(24px) saturate(180%) brightness(110%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid oklch(100% 0 0 / 0.15);
  border-top-color: oklch(100% 0 0 / 0.3);
  border-left-color: oklch(100% 0 0 / 0.2);
  box-shadow:
    0 4px 24px oklch(0% 0 0 / 0.12),
    0 1px 0 oklch(100% 0 0 / 0.1) inset,
    0 -1px 0 oklch(0% 0 0 / 0.05) inset;
}

/* Tinted glass */
.glass-blue {
  background: oklch(60% 0.2 260 / 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid oklch(60% 0.2 260 / 0.2);
}
```

## 7. Advanced Shadows & Depth
```css
/* Layered shadows for elevation */
.elevated-card {
  box-shadow:
    0 1px 2px oklch(0% 0 0 / 0.04),
    0 2px 4px oklch(0% 0 0 / 0.04),
    0 4px 8px oklch(0% 0 0 / 0.04),
    0 8px 16px oklch(0% 0 0 / 0.04),
    0 16px 32px oklch(0% 0 0 / 0.04);
}

/* Colored shadows — matches brand */
.primary-button {
  box-shadow:
    0 4px 16px var(--color-primary) / 0.4,
    0 1px 4px oklch(0% 0 0 / 0.1);
}

/* Inner glow */
.glow-card {
  box-shadow:
    inset 0 0 60px oklch(65% 0.25 260 / 0.1),
    0 0 0 1px oklch(65% 0.25 260 / 0.2);
}
```

## 8. Noise & Texture overlays
```css
/* SVG noise for organic texture */
.texture-overlay::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.05'/%3E%3C/svg%3E");
  mix-blend-mode: overlay;
  pointer-events: none;
}

/* Grain overlay using CSS filter */
.grain {
  position: relative;
}
.grain::after {
  content: "";
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,...");
  opacity: 0.03;
  mix-blend-mode: multiply;
  pointer-events: none;
}
```

## 9. CSS Custom Properties — advanced patterns
```css
/* Reactive properties with @property */
@property --gradient-angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}

.animated-gradient-border {
  background: conic-gradient(from var(--gradient-angle), #7c3aed, #3b82f6, #10b981, #7c3aed);
  animation: rotate-gradient 4s linear infinite;
}
@keyframes rotate-gradient {
  to { --gradient-angle: 360deg; }
}

/* Computed spacing scale */
:root {
  --space-unit: 0.25rem;
  --space-1: calc(var(--space-unit) * 1);   /* 4px */
  --space-2: calc(var(--space-unit) * 2);   /* 8px */
  --space-4: calc(var(--space-unit) * 4);   /* 16px */
  --space-6: calc(var(--space-unit) * 6);   /* 24px */
  --space-10: calc(var(--space-unit) * 10); /* 40px */
  --space-16: calc(var(--space-unit) * 16); /* 64px */
}
```

## 10. Clip-path animations
```css
/* Diagonal reveal */
.hero-reveal {
  clip-path: polygon(0 0, 0 0, 0 100%, 0 100%);
  animation: reveal-diagonal 0.8s cubic-bezier(0.77, 0, 0.175, 1) forwards;
}
@keyframes reveal-diagonal {
  to { clip-path: polygon(0 0, 105% 0, 100% 100%, 0 100%); }
}

/* Hover shape morphing */
.btn {
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
  transition: clip-path 0.4s cubic-bezier(0.77, 0, 0.175, 1);
}
.btn:hover {
  clip-path: polygon(4% 0, 100% 0, 96% 100%, 0 100%);
}
```

## 11. Fluid responsive type scale
```css
:root {
  --fluid-xs:   clamp(0.75rem, 0.5vw + 0.65rem, 0.875rem);
  --fluid-sm:   clamp(0.875rem, 0.6vw + 0.75rem, 1rem);
  --fluid-base: clamp(1rem, 0.8vw + 0.875rem, 1.25rem);
  --fluid-lg:   clamp(1.25rem, 1.5vw + 1rem, 1.75rem);
  --fluid-xl:   clamp(1.5rem, 2.5vw + 1rem, 2.5rem);
  --fluid-2xl:  clamp(2rem, 4vw + 1rem, 4rem);
  --fluid-3xl:  clamp(2.5rem, 6vw + 1rem, 6rem);
  --fluid-hero: clamp(3rem, 8vw + 1rem, 9rem);
}
```

## 12. Multi-layer mesh gradients
```css
.mesh-bg {
  background:
    radial-gradient(ellipse 80% 60% at 20% 30%, oklch(65% 0.25 260 / 0.4), transparent),
    radial-gradient(ellipse 60% 70% at 80% 70%, oklch(72% 0.28 160 / 0.3), transparent),
    radial-gradient(ellipse 70% 50% at 50% 50%, oklch(78% 0.22 300 / 0.2), transparent),
    oklch(12% 0.02 260);
}
```

## 13. Focus styles (accessibility + aesthetics)
```css
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 3px;
  border-radius: 4px;
  box-shadow: 0 0 0 4px var(--color-primary) / 0.2;
}

/* Custom focus ring that matches component shape */
.btn:focus-visible {
  outline: none;
  box-shadow:
    0 0 0 2px var(--color-bg),
    0 0 0 4px var(--color-primary),
    0 0 0 6px var(--color-primary) / 0.3;
}
```

## 14. CSS Houdini — Paint API (progressive enhancement)
```css
/* Falls back gracefully if unsupported */
@supports (background: paint(something)) {
  .confetti-button {
    background: paint(confetti);
    --confetti-density: 30;
    --confetti-colors: '#7c3aed, #3b82f6, #10b981';
  }
}
```

## Performance checklist
- Use `will-change: transform` on elements that animate, but sparingly
- Prefer `transform` and `opacity` — they're GPU-composited
- Use `content-visibility: auto` on off-screen sections
- Add `contain: layout style` to isolated components
- Use `@layer` to manage cascade without specificity wars
"""
