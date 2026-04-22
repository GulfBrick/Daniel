# AI Designer Agent

World-class UI/UX design powered by Claude Opus 4.7. Produces real, production-ready
HTML/CSS/JS files, stays on-brand across sessions, and **learns from your feedback**.

---

## Features

- **Professional designs** — Typography, color theory, layout, micro-interactions,
  accessibility — all applied automatically.
- **Brand consistency** — Save brand profiles (colors, fonts, personality) and every
  design respects them automatically.
- **Continuous learning** — Rate designs 1–5 stars. The agent stores what works,
  recalls successful patterns in future sessions, and adapts to your preferences.
- **Real files** — Every design is saved as a standalone HTML file you can open
  immediately in any browser.
- **Adaptive thinking** — Claude reasons through complex design decisions before
  producing output. Prompt caching keeps it fast after the first request.

---

## Setup

```bash
cd ai-designer-agent
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

---

## Usage

### Start designing
```bash
python main.py
```

### Design with brand context
```bash
python main.py --brand "Acme Corp"
```

### Create a brand profile first
```bash
python main.py --brand-wizard
```

---

## In-session commands

| Command | What it does |
|---|---|
| `/rate` | Rate the last design 1–5 ★ (teaches the agent your taste) |
| `/brand NAME` | Switch to a brand profile |
| `/list` | See all saved designs |
| `/patterns` | See learned design patterns |
| `/new` | Start a fresh conversation |
| `/help` | Show all commands |
| `/quit` | Exit |

---

## Example requests

```
Design a dark SaaS landing page with glassmorphism hero section
Create a dashboard for a fintech app with a clean minimal style
Build a mobile-first e-commerce product card with hover animations
Make a brutalist portfolio homepage with bold typography
Generate a design system — colors, typography, spacing tokens
Redesign that last one but warmer and more approachable
```

---

## How it learns

1. **Rate your designs** — `/rate` after each session stores what worked.
2. **Pattern library** — When a technique succeeds, the agent stores it as a named
   pattern that gets recalled in relevant future sessions.
3. **Brand memory** — Brand profiles persist across every session.
4. **Preference tracking** — Feedback notes (like "always use more whitespace") are
   stored and injected into the system context automatically.

---

## Project structure

```
ai-designer-agent/
├── main.py              # CLI entry point
├── agent.py             # Claude API integration, streaming, tool loop
├── memory.py            # Pattern storage and learning persistence
├── brand_manager.py     # Brand profile management
├── tools.py             # Tool implementations + schema definitions
├── knowledge_base/      # Persistent JSON storage (patterns, brands, history)
└── outputs/             # Generated HTML/CSS/JS design files
```

---

## Technical notes

- **Model**: Claude Opus 4.7 (`claude-opus-4-7`)
- **Thinking**: Adaptive (Claude decides when to reason deeply)
- **Effort**: High — balances intelligence and speed
- **Caching**: System prompt (~700 tokens) is cached after first request
- **Tools**: 7 tools — save design, store/search patterns, brand management, notes
