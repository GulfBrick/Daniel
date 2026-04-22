#!/usr/bin/env python3
"""AI Designer Agent — world-class UI/UX design with continuous learning."""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

load_dotenv()

console = Console()

OUTPUTS_DIR = Path(__file__).parent / "outputs"
KB_DIR = Path(__file__).parent / "knowledge_base"


# ── Startup checks ────────────────────────────────────────────────────────────


def ensure_dirs() -> None:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    KB_DIR.mkdir(exist_ok=True)


def check_api_key() -> None:
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print(
            Panel(
                "[bold red]ANTHROPIC_API_KEY not set.[/bold red]\n\n"
                "1. Copy [cyan].env.example[/cyan] to [cyan].env[/cyan]\n"
                "2. Add your API key from [link=https://console.anthropic.com]console.anthropic.com[/link]",
                title="Setup Required",
                border_style="red",
            )
        )
        sys.exit(1)


# ── Welcome banner ────────────────────────────────────────────────────────────


def show_banner() -> None:
    console.print(
        Panel.fit(
            "[bold]✦  AI Designer Agent  ✦[/bold]\n"
            "[dim]World-class UI/UX · On-brand · Learns as it goes[/dim]",
            border_style="bright_magenta",
            padding=(1, 4),
        )
    )
    console.print(
        "[dim]Powered by Claude Opus 4.7 · Designs saved to [cyan]outputs/[/cyan][/dim]\n"
    )


def show_help() -> None:
    console.print(
        Panel(
            "[bold]/rate[/bold]        — Rate the last design (1–5 ★)\n"
            "[bold]/brand NAME[/bold]  — Switch to a brand profile\n"
            "[bold]/list[/bold]        — List all saved designs\n"
            "[bold]/patterns[/bold]    — Show learned design patterns\n"
            "[bold]/new[/bold]         — Start a fresh conversation\n"
            "[bold]/help[/bold]        — Show this help\n"
            "[bold]/quit[/bold]        — Exit",
            title="Commands",
            border_style="dim",
        )
    )


# ── Brand wizard ──────────────────────────────────────────────────────────────


def run_brand_wizard() -> None:
    from brand_manager import BrandManager

    console.print(Panel.fit("[bold]Brand Profile Creator[/bold]", border_style="cyan"))
    console.print("[dim]Save brand guidelines so every design stays on-brand.\n[/dim]")

    bm = BrandManager()

    name = Prompt.ask("Brand name")
    tagline = Prompt.ask("Tagline / mission (optional)", default="")
    industry = Prompt.ask("Industry (e.g. SaaS, Fintech, Fashion)")
    personality = Prompt.ask(
        "Brand personality (e.g. bold and innovative, warm and approachable)"
    )
    tone = Prompt.ask("Tone of voice (e.g. professional, playful, authoritative)")
    primary = Prompt.ask("Primary color (hex, e.g. #6C63FF)")
    secondary = Prompt.ask("Secondary color (hex, e.g. #3ECFCF)")
    accent = Prompt.ask("Accent / CTA color (hex, e.g. #FF6B6B)")
    heading_font = Prompt.ask("Heading font (e.g. Inter, Playfair Display, Raleway)")
    body_font = Prompt.ask("Body font (e.g. Inter, Georgia, Source Serif 4)")
    do_list = Prompt.ask("Design DOs (optional)", default="")
    dont_list = Prompt.ask("Design DON'Ts (optional)", default="")
    notes = Prompt.ask("Any other notes (optional)", default="")

    profile: dict = {
        "tagline": tagline,
        "industry": industry,
        "personality": personality,
        "tone": tone,
        "colors": {
            "primary": primary,
            "secondary": secondary,
            "accent": accent,
        },
        "fonts": {"heading": heading_font, "body": body_font},
    }
    if do_list:
        profile["do"] = do_list
    if dont_list:
        profile["dont"] = dont_list
    if notes:
        profile["notes"] = notes

    bm.save_brand(name, profile)
    console.print(f"\n[bold green]✓ Brand '{name}' saved![/bold green]")
    console.print(
        f"[dim]Start designing: [cyan]python main.py --brand \"{name}\"[/cyan][/dim]\n"
    )


# ── Pattern viewer ────────────────────────────────────────────────────────────


def show_patterns() -> None:
    from memory import DesignMemory

    dm = DesignMemory()
    patterns = dm.get_top_patterns(limit=20)
    if not patterns:
        console.print("[dim]No patterns learned yet. Start designing![/dim]")
        return

    table = Table(title="Learned Design Patterns", border_style="dim")
    table.add_column("Name", style="bold cyan", no_wrap=True)
    table.add_column("Description")
    table.add_column("Tags", style="dim")
    table.add_column("Rating", justify="center")
    table.add_column("Uses", justify="center")

    for p in patterns:
        table.add_row(
            p["name"],
            p["description"][:80] + ("…" if len(p["description"]) > 80 else ""),
            ", ".join(p.get("tags", [])[:4]),
            str(p.get("rating", "—")),
            str(p.get("uses", 0)),
        )
    console.print(table)


# ── Main interactive loop ─────────────────────────────────────────────────────


def run_interactive(brand_name: str | None = None) -> None:
    from agent import DesignerAgent

    show_banner()

    if brand_name:
        from brand_manager import BrandManager

        bm = BrandManager()
        if bm.get_brand(brand_name):
            console.print(
                f"[bold green]✓ Brand context loaded:[/bold green] [cyan]{brand_name}[/cyan]\n"
            )
        else:
            console.print(
                f"[yellow]⚠ No brand profile for '{brand_name}' — "
                f"run [bold]python main.py --brand-wizard[/bold] to create one.[/yellow]\n"
            )

    agent = DesignerAgent(brand_name=brand_name)

    console.print("[dim]Type your design request, or [bold]/help[/bold] for commands.[/dim]\n")

    while True:
        try:
            user_input = Prompt.ask("[bold magenta]You[/bold magenta]").strip()

            if not user_input:
                continue

            # ── Commands ──────────────────────────────────────────────────────

            if user_input.lower() in ("/quit", "/exit", "quit", "exit"):
                console.print(
                    "[dim]Session ended. Your designs are in [cyan]outputs/[/cyan][/dim]"
                )
                break

            if user_input.lower() == "/help":
                show_help()
                continue

            if user_input.lower() == "/new":
                agent.conversation_history = []
                console.print("[green]✓ Fresh conversation started.[/green]")
                continue

            if user_input.lower() == "/list":
                designs = sorted(
                    OUTPUTS_DIR.glob("*.html"),
                    key=lambda f: f.stat().st_mtime,
                    reverse=True,
                )
                if not designs:
                    console.print("[dim]No designs saved yet.[/dim]")
                else:
                    table = Table(title="Saved Designs", border_style="dim")
                    table.add_column("File", style="cyan")
                    table.add_column("Size", justify="right", style="dim")
                    for d in designs[:15]:
                        sz = d.stat().st_size
                        size_str = f"{sz // 1024} KB" if sz > 1024 else f"{sz} B"
                        table.add_row(d.name, size_str)
                    console.print(table)
                continue

            if user_input.lower() == "/patterns":
                show_patterns()
                continue

            if user_input.lower() == "/rate":
                rating = IntPrompt.ask("Rate the last design (1–5 ★)", default=5)
                rating = max(1, min(5, rating))
                feedback = Prompt.ask("Feedback (optional)", default="")
                agent.rate_last_design(rating, feedback)
                stars = "★" * rating + "☆" * (5 - rating)
                console.print(f"[bold]Rated:[/bold] {stars} — thanks, I'll remember that!")
                continue

            if user_input.lower().startswith("/brand"):
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2:
                    console.print("Usage: [bold]/brand NAME[/bold]")
                else:
                    agent.brand_name = parts[1]
                    console.print(
                        f"[green]✓ Brand switched to:[/green] [cyan]{parts[1]}[/cyan]"
                    )
                continue

            # ── Design request ─────────────────────────────────────────────────

            console.print(f"\n[bold cyan]Designer[/bold cyan]  ", end="")
            agent.chat(user_input)
            console.print()  # spacer

        except KeyboardInterrupt:
            console.print(
                "\n\n[dim]Interrupted. Your work is saved in [cyan]outputs/[/cyan][/dim]"
            )
            break
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {e}")
            import traceback

            console.print(f"[dim]{traceback.format_exc()}[/dim]")


# ── Entry point ───────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI Designer Agent — world-class UI/UX powered by Claude",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                        # Start designing
  python main.py --brand "Acme Corp"    # Design with brand context
  python main.py --brand-wizard         # Create a brand profile
  python main.py --list-designs         # List saved designs
  python main.py --show-patterns        # Show learned patterns
        """,
    )
    parser.add_argument("--brand", metavar="NAME", help="Brand profile to use")
    parser.add_argument(
        "--brand-wizard", action="store_true", help="Create a new brand profile"
    )
    parser.add_argument(
        "--list-designs", action="store_true", help="List all saved designs and exit"
    )
    parser.add_argument(
        "--show-patterns", action="store_true", help="Show learned design patterns and exit"
    )

    args = parser.parse_args()

    ensure_dirs()
    check_api_key()

    if args.brand_wizard:
        run_brand_wizard()
    elif args.list_designs:
        designs = sorted(
            OUTPUTS_DIR.glob("*.html"),
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )
        if not designs:
            console.print("[dim]No designs saved yet.[/dim]")
        else:
            for d in designs:
                sz = d.stat().st_size
                size_str = f"{sz // 1024} KB" if sz > 1024 else f"{sz} B"
                console.print(f"[cyan]{d.name}[/cyan]  [dim]{size_str}[/dim]")
    elif args.show_patterns:
        show_patterns()
    else:
        run_interactive(brand_name=args.brand)


if __name__ == "__main__":
    main()
