"""Tool implementations — what the agent can actually do."""

import json
import re
import time
from pathlib import Path

from memory import DesignMemory
from brand_manager import BrandManager

OUTPUTS_DIR = Path(__file__).parent / "outputs"


class DesignTools:
    """Executes tool calls made by the agent."""

    def __init__(self, memory: DesignMemory, brand_manager: BrandManager):
        self.memory = memory
        self.brand_manager = brand_manager
        OUTPUTS_DIR.mkdir(exist_ok=True)

    # ── Dispatch ───────────────────────────────────────────────────────────────

    def execute(self, name: str, inputs: dict) -> str:
        handlers = {
            "save_design": self._save_design,
            "store_pattern": self._store_pattern,
            "search_patterns": self._search_patterns,
            "get_brand": self._get_brand,
            "update_brand": self._update_brand,
            "list_designs": self._list_designs,
            "record_design_note": self._record_design_note,
        }
        handler = handlers.get(name)
        if not handler:
            return f"Unknown tool: {name}"
        try:
            return handler(**inputs)
        except TypeError as e:
            return f"Tool error ({name}): {e}"
        except Exception as e:
            return f"Tool failed ({name}): {e}"

    # ── Tool implementations ───────────────────────────────────────────────────

    def _save_design(
        self,
        filename: str,
        html: str,
        description: str = "",
        preview_note: str = "",
    ) -> str:
        # Sanitise filename
        safe = re.sub(r"[^a-zA-Z0-9_\-]", "_", filename.replace(".html", ""))
        timestamp = int(time.time())
        filepath = OUTPUTS_DIR / f"{safe}_{timestamp}.html"
        filepath.write_text(html, encoding="utf-8")

        # Record in history
        self.memory.record_interaction(
            user_request="",  # filled by agent context
            design_description=description or filename,
            output_file=str(filepath),
        )

        note = f" Preview note: {preview_note}" if preview_note else ""
        return (
            f"Design saved to: outputs/{filepath.name}{note}\n"
            f"Open the file in any browser to preview the design."
        )

    def _store_pattern(
        self,
        name: str,
        description: str,
        tags: list | None = None,
        code_snippet: str = "",
    ) -> str:
        return self.memory.store_pattern(
            name=name,
            description=description,
            tags=tags or [],
            code_snippet=code_snippet,
        )

    def _search_patterns(self, query: str, tags: list | None = None) -> str:
        results = self.memory.search_patterns(query, tags)
        if not results:
            return "No matching patterns found."
        output = []
        for p in results:
            output.append(
                f"**{p['name']}** (rating: {p.get('rating', 0)}, uses: {p.get('uses', 0)})\n"
                f"  {p['description']}\n"
                f"  Tags: {', '.join(p.get('tags', []))}"
            )
            if p.get("code_snippet"):
                output.append(f"  Snippet:\n```\n{p['code_snippet'][:300]}\n```")
        return "\n\n".join(output)

    def _get_brand(self, brand_name: str) -> str:
        brand = self.brand_manager.get_brand(brand_name)
        if not brand:
            return f"No brand profile found for '{brand_name}'."
        return json.dumps(brand, indent=2)

    def _update_brand(self, brand_name: str, **fields) -> str:
        return self.brand_manager.update_brand(brand_name, fields)

    def _list_designs(self) -> str:
        designs = sorted(OUTPUTS_DIR.glob("*.html"), key=lambda f: f.stat().st_mtime, reverse=True)
        if not designs:
            return "No designs saved yet."
        lines = [f"Saved designs ({len(designs)} total):"]
        for d in designs[:15]:
            size = d.stat().st_size
            size_str = f"{size // 1024}KB" if size > 1024 else f"{size}B"
            lines.append(f"  - {d.name} ({size_str})")
        return "\n".join(lines)

    def _record_design_note(self, note: str, context: str = "") -> str:
        # Store as a special pattern tagged as a user preference note
        name = f"preference_note_{int(time.time())}"
        self.memory.store_pattern(
            name=name,
            description=note,
            tags=["preference", "note", "user-feedback"],
            code_snippet=context,
        )
        return f"Note recorded: {note}"


# ── Tool schema definitions (passed to Claude) ──────────────────────────────

TOOL_DEFINITIONS = [
    {
        "name": "save_design",
        "description": (
            "Save a complete HTML/CSS/JS design to the outputs folder. "
            "Use this whenever you produce a finished design — it writes the file and "
            "confirms the path so the user can open it in a browser."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Descriptive filename without extension (e.g. 'hero-landing', 'dashboard-dark')",
                },
                "html": {
                    "type": "string",
                    "description": "Complete, standalone HTML document with embedded CSS and JS",
                },
                "description": {
                    "type": "string",
                    "description": "One-sentence description of what this design is",
                },
                "preview_note": {
                    "type": "string",
                    "description": "Any special note about opening or interacting with the design",
                },
            },
            "required": ["filename", "html"],
        },
    },
    {
        "name": "store_pattern",
        "description": (
            "Store a successful design pattern in the knowledge base so it can be recalled in future sessions. "
            "Use this when a particular approach, technique, or aesthetic worked well."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Short unique name for this pattern",
                },
                "description": {
                    "type": "string",
                    "description": "What this pattern is, when to use it, and why it works",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tags like 'dark-mode', 'glassmorphism', 'card', 'hero', 'dashboard'",
                },
                "code_snippet": {
                    "type": "string",
                    "description": "Key CSS or HTML snippet that captures the essence of this pattern",
                },
            },
            "required": ["name", "description"],
        },
    },
    {
        "name": "search_patterns",
        "description": (
            "Search the knowledge base for past design patterns relevant to the current task. "
            "Call this at the start of complex design requests to leverage past learnings."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "What you're looking for (e.g. 'navigation bar', 'card hover effects')",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional tag filters to narrow results",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_brand",
        "description": (
            "Retrieve a brand profile from the knowledge base. "
            "Use this when the user mentions a brand name and you need its colors, fonts, and guidelines."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "brand_name": {
                    "type": "string",
                    "description": "The brand name to look up",
                },
            },
            "required": ["brand_name"],
        },
    },
    {
        "name": "update_brand",
        "description": (
            "Create or update a brand profile in the knowledge base. "
            "Use this when the user describes their brand or wants to save brand guidelines."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "brand_name": {
                    "type": "string",
                    "description": "The brand name",
                },
                "tagline": {"type": "string"},
                "industry": {"type": "string"},
                "personality": {
                    "type": "string",
                    "description": "Brand personality (e.g. 'bold and innovative', 'warm and friendly')",
                },
                "tone": {
                    "type": "string",
                    "description": "Communication tone (e.g. 'professional', 'playful', 'authoritative')",
                },
                "colors": {
                    "type": "object",
                    "description": "Color map: {primary, secondary, accent, background, text}",
                },
                "fonts": {
                    "type": "object",
                    "description": "Font map: {heading, body, mono}",
                },
                "do": {
                    "type": "string",
                    "description": "Design DOs for this brand",
                },
                "dont": {
                    "type": "string",
                    "description": "Design DON'Ts for this brand",
                },
                "notes": {
                    "type": "string",
                    "description": "Any other brand notes or special instructions",
                },
            },
            "required": ["brand_name"],
        },
    },
    {
        "name": "list_designs",
        "description": "List all previously saved design files in the outputs folder.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "record_design_note",
        "description": (
            "Record a user preference or design note that should influence future work. "
            "Use this when the user expresses a preference, style direction, or correction "
            "that should be remembered long-term."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "note": {
                    "type": "string",
                    "description": "The preference or insight to remember",
                },
                "context": {
                    "type": "string",
                    "description": "What was happening when this note was made",
                },
            },
            "required": ["note"],
        },
    },
]
