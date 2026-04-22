"""Brand profile management — keep designs on-brand across sessions."""

import json
from pathlib import Path


KB_DIR = Path(__file__).parent / "knowledge_base"
PROFILES_PATH = KB_DIR / "brand_profiles.json"


class BrandManager:
    """Create, update, and retrieve brand profiles."""

    def __init__(self):
        KB_DIR.mkdir(exist_ok=True)

    def _load(self) -> dict:
        try:
            return json.loads(PROFILES_PATH.read_text()) if PROFILES_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            return {}

    def _save(self, data: dict) -> None:
        PROFILES_PATH.write_text(json.dumps(data, indent=2))

    def save_brand(self, name: str, profile: dict) -> str:
        profiles = self._load()
        profiles[name.lower()] = {**profile, "name": name}
        self._save(profiles)
        return f"Brand '{name}' saved."

    def get_brand(self, name: str) -> dict | None:
        profiles = self._load()
        return profiles.get(name.lower())

    def update_brand(self, name: str, updates: dict) -> str:
        profiles = self._load()
        key = name.lower()
        if key not in profiles:
            profiles[key] = {"name": name}
        profiles[key].update(updates)
        self._save(profiles)
        return f"Brand '{name}' updated."

    def list_brands(self) -> list[str]:
        return list(self._load().keys())

    def brand_to_prompt_context(self, name: str) -> str:
        """Format a brand profile as a system prompt section."""
        brand = self.get_brand(name)
        if not brand:
            return f"No brand profile found for '{name}'. Design with a professional default aesthetic."

        lines = [f"## Active Brand: {brand.get('name', name)}"]
        if brand.get("tagline"):
            lines.append(f"**Tagline:** {brand['tagline']}")
        if brand.get("industry"):
            lines.append(f"**Industry:** {brand['industry']}")
        if brand.get("personality"):
            lines.append(f"**Personality:** {brand['personality']}")
        if brand.get("tone"):
            lines.append(f"**Tone of voice:** {brand['tone']}")
        if brand.get("colors"):
            c = brand["colors"]
            lines.append("**Brand colors:**")
            for role, hex_val in c.items():
                lines.append(f"  - {role}: {hex_val}")
        if brand.get("fonts"):
            f = brand["fonts"]
            lines.append("**Typography:**")
            for role, font in f.items():
                lines.append(f"  - {role}: {font}")
        if brand.get("do"):
            lines.append(f"**Design DO:** {brand['do']}")
        if brand.get("dont"):
            lines.append(f"**Design DON'T:** {brand['dont']}")
        if brand.get("notes"):
            lines.append(f"**Additional notes:** {brand['notes']}")

        lines.append(
            "\nAlways respect these guidelines in every design. "
            "Use the exact brand colors, fonts, and personality. "
            "Never deviate from the brand identity without explicit instruction."
        )
        return "\n".join(lines)
