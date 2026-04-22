"""Persistent learning and memory system for the designer agent."""

import json
import time
from pathlib import Path
from typing import Any


KB_DIR = Path(__file__).parent / "knowledge_base"


class DesignMemory:
    """Stores and retrieves design patterns, history, and learnings."""

    def __init__(self):
        KB_DIR.mkdir(exist_ok=True)
        self._patterns_path = KB_DIR / "design_patterns.json"
        self._history_path = KB_DIR / "design_history.json"

    def _load(self, path: Path) -> Any:
        try:
            return json.loads(path.read_text()) if path.exists() else []
        except (json.JSONDecodeError, OSError):
            return []

    def _save(self, path: Path, data: Any) -> None:
        path.write_text(json.dumps(data, indent=2))

    # ── Patterns ──────────────────────────────────────────────────────────────

    def store_pattern(
        self,
        name: str,
        description: str,
        tags: list[str],
        code_snippet: str = "",
        rating: int = 0,
    ) -> str:
        patterns = self._load(self._patterns_path)
        # Overwrite if same name exists
        patterns = [p for p in patterns if p.get("name") != name]
        patterns.append(
            {
                "name": name,
                "description": description,
                "tags": [t.lower() for t in tags],
                "code_snippet": code_snippet,
                "rating": rating,
                "uses": 1,
                "timestamp": time.time(),
            }
        )
        self._save(self._patterns_path, patterns)
        return f"Pattern '{name}' stored."

    def search_patterns(self, query: str, tags: list[str] | None = None) -> list[dict]:
        patterns = self._load(self._patterns_path)
        q = query.lower()
        results = []
        for p in patterns:
            score = 0
            if q in p.get("name", "").lower():
                score += 3
            if q in p.get("description", "").lower():
                score += 2
            if tags:
                matched = sum(1 for t in tags if t.lower() in p.get("tags", []))
                score += matched * 2
            # Boost by rating and recency
            score += p.get("rating", 0) * 0.5
            if score > 0:
                results.append({**p, "_score": score})
        results.sort(key=lambda x: x["_score"], reverse=True)
        return results[:5]

    def get_top_patterns(self, limit: int = 5) -> list[dict]:
        patterns = self._load(self._patterns_path)
        # Sort by rating then uses
        patterns.sort(key=lambda p: (p.get("rating", 0), p.get("uses", 0)), reverse=True)
        return patterns[:limit]

    def increment_pattern_uses(self, name: str) -> None:
        patterns = self._load(self._patterns_path)
        for p in patterns:
            if p.get("name") == name:
                p["uses"] = p.get("uses", 0) + 1
                break
        self._save(self._patterns_path, patterns)

    # ── History & Ratings ─────────────────────────────────────────────────────

    def record_interaction(
        self,
        user_request: str,
        design_description: str,
        output_file: str = "",
    ) -> int:
        history = self._load(self._history_path)
        entry = {
            "id": len(history),
            "timestamp": time.time(),
            "user_request": user_request[:500],
            "design_description": design_description[:500],
            "output_file": output_file,
            "rating": None,
            "feedback": "",
        }
        history.append(entry)
        self._save(self._history_path, history)
        return entry["id"]

    def record_rating(self, entry_id: int, rating: int, feedback: str = "") -> str:
        history = self._load(self._history_path)
        for entry in history:
            if entry.get("id") == entry_id:
                entry["rating"] = rating
                entry["feedback"] = feedback
                break
        self._save(self._history_path, history)
        return f"Rating {rating}/5 recorded."

    def get_last_entry_id(self) -> int | None:
        history = self._load(self._history_path)
        return history[-1]["id"] if history else None

    def get_recent_history(self, limit: int = 10) -> list[dict]:
        history = self._load(self._history_path)
        return history[-limit:]

    def get_preferences_summary(self) -> str:
        """Summarise what the user has consistently rated highly."""
        history = self._load(self._history_path)
        rated = [h for h in history if h.get("rating") is not None]
        if not rated:
            return ""
        high = [h for h in rated if h["rating"] >= 4]
        low = [h for h in rated if h["rating"] <= 2]
        lines = []
        if high:
            lines.append(
                f"Previously well-received designs ({len(high)} entries): "
                + "; ".join(h["design_description"][:80] for h in high[-3:])
            )
        if low:
            lines.append(
                f"Designs that missed the mark ({len(low)} entries): "
                + "; ".join(h["design_description"][:80] for h in low[-3:])
            )
        return "\n".join(lines)
