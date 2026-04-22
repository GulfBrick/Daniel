"""Skill registry — modular design knowledge loaded on demand."""

from pathlib import Path
import importlib

SKILL_REGISTRY = {
    "framer_motion": "skills.framer_motion",
    "gsap": "skills.gsap",
    "advanced_css": "skills.advanced_css",
    "innovation": "skills.innovation",
}


def load_skill(name: str) -> str:
    """Return the full documentation string for a skill."""
    key = name.lower().replace("-", "_").replace(" ", "_")
    module_path = SKILL_REGISTRY.get(key)
    if not module_path:
        available = ", ".join(SKILL_REGISTRY.keys())
        return f"Skill '{name}' not found. Available skills: {available}"
    mod = importlib.import_module(module_path)
    return getattr(mod, "SKILL_DOCS", f"Skill '{name}' has no SKILL_DOCS.")


def list_skills() -> list[str]:
    return list(SKILL_REGISTRY.keys())
