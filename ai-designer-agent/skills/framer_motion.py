"""Framer Motion skill — animation recipes for React-based designs."""

SKILL_DOCS = """
# FRAMER MOTION MASTERY

Framer Motion is a production-ready animation library for React. When building React designs,
use Framer Motion for all animations. Here are the essential patterns:

## CDN Setup (for standalone HTML)
```html
<script src="https://unpkg.com/react@18/umd/react.development.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
<script src="https://unpkg.com/framer-motion@11/dist/framer-motion.js"></script>
```

Access via: `window.FramerMotion.motion`, `window.FramerMotion.AnimatePresence` etc.

## Core Concepts

### 1. Basic motion elements
```jsx
import { motion } from "framer-motion";

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.4, ease: [0.25, 0.46, 0.45, 0.94] }}
/>
```

### 2. Variants — the RIGHT way to coordinate animations
```jsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 24, filter: "blur(4px)" },
  visible: {
    opacity: 1,
    y: 0,
    filter: "blur(0px)",
    transition: { duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] },
  },
};

<motion.ul variants={containerVariants} initial="hidden" animate="visible">
  {items.map((item) => (
    <motion.li key={item.id} variants={itemVariants}>
      {item.content}
    </motion.li>
  ))}
</motion.ul>
```

### 3. Gesture animations — hover, tap, drag
```jsx
<motion.button
  whileHover={{ scale: 1.04, y: -2, boxShadow: "0 16px 48px rgba(0,0,0,0.2)" }}
  whileTap={{ scale: 0.97 }}
  transition={{ type: "spring", stiffness: 400, damping: 25 }}
/>

// Magnetic button effect
const [pos, setPos] = useState({ x: 0, y: 0 });
<motion.button
  animate={pos}
  onMouseMove={(e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = (e.clientX - rect.left - rect.width / 2) * 0.3;
    const y = (e.clientY - rect.top - rect.height / 2) * 0.3;
    setPos({ x, y });
  }}
  onMouseLeave={() => setPos({ x: 0, y: 0 })}
/>
```

### 4. AnimatePresence — smooth mount/unmount
```jsx
import { AnimatePresence, motion } from "framer-motion";

<AnimatePresence mode="wait">
  {isOpen && (
    <motion.div
      key="modal"
      initial={{ opacity: 0, scale: 0.95, y: 10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95, y: 10 }}
      transition={{ duration: 0.2, ease: "easeOut" }}
    />
  )}
</AnimatePresence>

// Page transitions
<AnimatePresence mode="wait">
  <motion.main
    key={currentPage}
    initial={{ opacity: 0, x: 20 }}
    animate={{ opacity: 1, x: 0 }}
    exit={{ opacity: 0, x: -20 }}
    transition={{ duration: 0.3 }}
  />
</AnimatePresence>
```

### 5. Scroll animations — useInView
```jsx
import { motion, useInView } from "framer-motion";
import { useRef } from "react";

function RevealOnScroll({ children }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-80px" });
  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 40 }}
      transition={{ duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] }}
    >
      {children}
    </motion.div>
  );
}
```

### 6. Scroll-linked motion — useScroll + useTransform
```jsx
import { useScroll, useTransform, motion } from "framer-motion";

function ParallaxHero() {
  const { scrollY } = useScroll();
  const y = useTransform(scrollY, [0, 500], [0, -150]);
  const opacity = useTransform(scrollY, [0, 300], [1, 0]);
  const scale = useTransform(scrollY, [0, 300], [1, 1.1]);

  return (
    <motion.div style={{ y, opacity, scale }}>
      <h1>Hero Section</h1>
    </motion.div>
  );
}

// Section-level progress bar
function ProgressBar() {
  const { scrollYProgress } = useScroll();
  return <motion.div style={{ scaleX: scrollYProgress }} className="progress-bar" />;
}
```

### 7. Layout animations — automatic layout transitions
```jsx
// Add layoutId to animate elements between positions
<motion.div layoutId="hero-image" />
// Clicking navigates to detail view:
<motion.img layoutId="hero-image" src={img} />

// Layout prop animates size changes
<motion.ul layout>
  {items.map(item => (
    <motion.li key={item.id} layout exit={{ opacity: 0 }}>
      {item.content}
    </motion.li>
  ))}
</motion.ul>
```

### 8. useMotionValue + useSpring — smooth cursor tracking
```jsx
import { useMotionValue, useSpring, motion } from "framer-motion";

function CustomCursor() {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);
  const springX = useSpring(mouseX, { stiffness: 150, damping: 15 });
  const springY = useSpring(mouseY, { stiffness: 150, damping: 15 });

  useEffect(() => {
    const move = (e) => { mouseX.set(e.clientX); mouseY.set(e.clientY); };
    window.addEventListener("mousemove", move);
    return () => window.removeEventListener("mousemove", move);
  }, []);

  return (
    <motion.div
      className="cursor"
      style={{ x: springX, y: springY, translateX: "-50%", translateY: "-50%" }}
    />
  );
}
```

### 9. Text animations — character by character
```jsx
function AnimatedText({ text }) {
  const words = text.split(" ");
  return (
    <motion.p
      variants={{ visible: { transition: { staggerChildren: 0.05 } } }}
      initial="hidden"
      animate="visible"
    >
      {words.map((word, i) => (
        <motion.span
          key={i}
          style={{ display: "inline-block", marginRight: "0.25em" }}
          variants={{
            hidden: { opacity: 0, y: 20, rotateX: -90 },
            visible: { opacity: 1, y: 0, rotateX: 0, transition: { duration: 0.4 } },
          }}
        >
          {word}
        </motion.span>
      ))}
    </motion.p>
  );
}
```

### 10. Spring configs — the right feel for the right context
```js
// Snappy UI (buttons, toggles)
{ type: "spring", stiffness: 500, damping: 30 }

// Smooth content (cards, panels)
{ type: "spring", stiffness: 300, damping: 25 }

// Bouncy/playful
{ type: "spring", stiffness: 200, damping: 12 }

// Slow, luxurious
{ duration: 0.8, ease: [0.25, 0.46, 0.45, 0.94] }

// Material-style
{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }
```

### 11. Drag interactions
```jsx
<motion.div
  drag
  dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
  dragElastic={0.1}
  whileDrag={{ scale: 1.05, cursor: "grabbing" }}
  onDragEnd={(e, info) => console.log(info.offset, info.velocity)}
/>

// Carousel
<motion.div
  drag="x"
  dragConstraints={{ left: -(width - containerWidth), right: 0 }}
  style={{ x: dragX }}
/>
```

## Production Patterns

### Card stack with hover reveal
```jsx
function CardStack({ cards }) {
  const [hoveredIndex, setHoveredIndex] = useState(null);
  return (
    <div style={{ position: "relative" }}>
      {cards.map((card, i) => (
        <motion.div
          key={card.id}
          style={{ position: "absolute" }}
          animate={{
            top: hoveredIndex === i ? -20 : i * 8,
            zIndex: hoveredIndex === i ? 10 : i,
            scale: hoveredIndex === i ? 1.02 : 1 - i * 0.02,
          }}
          onHoverStart={() => setHoveredIndex(i)}
          onHoverEnd={() => setHoveredIndex(null)}
        />
      ))}
    </div>
  );
}
```

### Number counter animation
```jsx
function Counter({ from, to, duration = 2 }) {
  const count = useMotionValue(from);
  const rounded = useTransform(count, (v) => Math.round(v).toLocaleString());
  useEffect(() => {
    animate(count, to, { duration, ease: "easeOut" });
  }, []);
  return <motion.span>{rounded}</motion.span>;
}
```
"""
