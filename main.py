"""
Tech Pulse -- Tech Job Trends Agent
===================================
On-demand agent that collects tech job market data across North America,
processes it into analytics, generates career insights, and renders
an interactive HTML dashboard.

Usage:
    python main.py                  Full run (collect -> analyze -> dashboard)
    python main.py --collect-only   Only fetch new data
    python main.py --dashboard-only Regenerate dashboard from cached data
    python main.py --no-api         Skip SerpApi (web scraping + curated data only)
    python main.py --no-browser     Don't auto-open the dashboard
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import config
import collector
import analytics
import insights
import dashboard

console = Console(force_terminal=True)


def _load_cached_analytics() -> dict | None:
    """Load the most recent processed analytics from disk."""
    path = config.PROCESSED_DIR / "analytics.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _load_cached_raw() -> dict | None:
    """Load the most recent raw data from disk."""
    raw_files = sorted(config.RAW_DIR.glob("raw_*.json"), reverse=True)
    if raw_files:
        with open(raw_files[0], "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def run(
    use_api: bool = True,
    collect_only: bool = False,
    dashboard_only: bool = False,
    open_browser: bool = True,
) -> None:
    """Main execution pipeline."""
    start = time.time()

    console.print()
    console.print(
        Panel(
            "[bold]Tech Job Trends Agent -- North America[/]",
            title="[bold cyan]TECH PULSE[/]",
            style="cyan",
            padding=(1, 4),
        )
    )
    console.print()

    if dashboard_only:
        # ── Dashboard-only mode ────────────────────────────────────────
        console.print(Panel("📊 Dashboard-only mode — using cached data", style="blue"))
        analytics_data = _load_cached_analytics()
        if not analytics_data:
            console.print("[red]✗ No cached analytics found. Run a full collection first.[/]")
            sys.exit(1)

        # Re-generate insights from cached analytics
        insights_data = insights.generate(analytics_data)
        dashboard.generate(analytics_data, insights_data, open_browser=open_browser)

    else:
        # ── Collection ─────────────────────────────────────────────────
        console.print(
            Panel(
                f"🔍 Collecting data… (API: {'enabled' if use_api else 'disabled'})",
                style="blue",
            )
        )
        raw_data = collector.collect_all(use_api=use_api)

        if collect_only:
            console.print("[green]✓ Collection complete. Use --dashboard-only to generate dashboard.[/]")
            elapsed = time.time() - start
            console.print(f"\n⏱  Finished in {elapsed:.1f}s")
            return

        # ── Analysis ───────────────────────────────────────────────────
        console.print(Panel("📊 Processing analytics…", style="blue"))
        analytics_data = analytics.process(raw_data)

        # ── Insights ───────────────────────────────────────────────────
        console.print(Panel("🔮 Generating career insights…", style="blue"))
        insights_data = insights.generate(analytics_data)

        # ── Dashboard ──────────────────────────────────────────────────
        console.print(Panel("🎨 Building dashboard…", style="blue"))
        out = dashboard.generate(analytics_data, insights_data, open_browser=open_browser)
        console.print()
        console.print(
            Panel(
                Text.from_markup(
                    f"[bold green]✓ Dashboard ready![/]\n\n"
                    f"  📄 [link=file://{out.resolve()}]{out}[/link]\n\n"
                    f"  Open the file above in your browser to view the dashboard."
                ),
                title="Tech Pulse",
                style="green",
            )
        )

    elapsed = time.time() - start
    console.print(f"\n⏱  Finished in {elapsed:.1f}s\n")


def main():
    parser = argparse.ArgumentParser(
        prog="techpulse",
        description="Tech Pulse — on-demand tech job trends agent for North America",
    )
    parser.add_argument(
        "--no-api",
        action="store_true",
        help="Skip SerpApi calls (uses web scraping + curated data)",
    )
    parser.add_argument(
        "--collect-only",
        action="store_true",
        help="Only collect data, don't generate dashboard",
    )
    parser.add_argument(
        "--dashboard-only",
        action="store_true",
        help="Regenerate dashboard from cached analytics",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Don't auto-open the dashboard in the browser",
    )
    args = parser.parse_args()

    run(
        use_api=not args.no_api,
        collect_only=args.collect_only,
        dashboard_only=args.dashboard_only,
        open_browser=not args.no_browser,
    )


if __name__ == "__main__":
    main()
