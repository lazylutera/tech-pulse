"""
Dashboard generator — renders the Jinja2 HTML template with analytics data.
"""
import json
import os
import webbrowser
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from rich.console import Console

import config

console = Console()


def _trend_implication(trend_name: str) -> str:
    """Get career implication text for a trend."""
    implications = {
        "AI Agents & Autonomous Systems": "Engineers who can design and orchestrate multi-agent systems will be among the most sought-after in tech.",
        "LLM Fine-tuning & RAG": "RAG is becoming the standard architecture for enterprise AI — learn vector DBs and embedding pipelines.",
        "Platform Engineering": "The evolution of DevOps into standardized, self-service internal platforms.",
        "Prompt Engineering": "Advanced prompt engineering for complex chains and agent workflows remains valuable.",
        "Zero Trust Security": "Every organization is migrating to Zero Trust. Security + cloud skills is a premium combination.",
        "Edge AI / TinyML": "Engineers who can optimize models for edge deployment will fill a critical skill gap.",
        "Rust for Systems Programming": "Rust's memory safety guarantees are making it the default for new infrastructure.",
        "Sustainability / Green Tech": "Carbon-aware computing and energy-efficient ML training are emerging specializations.",
        "Quantum Computing Readiness": "Quantum-safe cryptography and hybrid quantum-classical algorithms will need specialists.",
        "Multimodal AI": "AI systems that process text, image, audio, and video together — expect explosive demand.",
    }
    return implications.get(trend_name, "Emerging area with significant growth potential.")


def generate(analytics: dict, insights: dict, open_browser: bool = True) -> Path:
    """
    Render the HTML dashboard from analytics and insights data.
    Returns the path to the generated HTML file.
    """
    console.print("[cyan]🎨 Generating dashboard…[/]")

    env = Environment(
        loader=FileSystemLoader(str(config.TEMPLATES_DIR)),
        autoescape=False,
    )
    template = env.get_template("dashboard.html")

    # Prepare emerging trends with implications for the table
    emerging_trends_display = []
    for t in analytics.get("emerging_trends", []):
        emerging_trends_display.append({
            "trend": t["trend"],
            "growth": t.get("growth", ""),
            "maturity": t.get("maturity", ""),
            "implication": _trend_implication(t["trend"]),
        })

    # Render template
    html = template.render(
        generated_at=analytics.get("generated_at", ""),
        market_snapshot=analytics.get("market_snapshot", {}),
        top_skills=analytics.get("top_skills", []),
        data_sources=analytics.get("data_sources", []),
        live_jobs_count=analytics.get("live_jobs_count", 0),
        emerging_trends_display=emerging_trends_display,
        insights=insights,
        # JSON data for Chart.js
        top_skills_json=json.dumps(analytics.get("top_skills", [])[:20]),
        categories_json=json.dumps(analytics.get("skill_categories", [])),
        roles_json=json.dumps(analytics.get("roles", [])),
        salary_json=json.dumps(analytics.get("salary_data", [])),
        locations_json=json.dumps(analytics.get("locations", [])),
        radar_json=json.dumps(insights.get("radar_data", [])),
        growth_json=json.dumps(analytics.get("fastest_growing_skills", [])[:15]),
    )

    # Save
    out_path = config.OUTPUT_DIR / "dashboard.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    console.print(f"[green]✓ Dashboard saved → {out_path}[/]")

    if open_browser:
        file_url = out_path.resolve().as_uri()
        console.print(f"[cyan]🌐 Opening in browser…[/]")
        webbrowser.open(file_url)

    return out_path
