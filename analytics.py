"""
Analytics engine — processes raw job data into structured insights.
"""
import json
import re
from collections import Counter, defaultdict
from datetime import datetime

from rich.console import Console

import config

console = Console()


def _extract_skills_from_descriptions(jobs: list[dict]) -> Counter:
    """Parse job descriptions and count skill mentions."""
    skill_counter: Counter = Counter()
    all_skills: dict[str, str] = {}  # keyword -> category
    for cat, keywords in config.SKILL_CATEGORIES.items():
        for kw in keywords:
            all_skills[kw.lower()] = cat

    for job in jobs:
        desc = (job.get("description", "") + " " + job.get("title", "")).lower()
        seen_in_job: set[str] = set()
        for kw, cat in all_skills.items():
            if kw in desc and kw not in seen_in_job:
                skill_counter[kw] += 1
                seen_in_job.add(kw)

    return skill_counter


def _categorize_skills(skill_counts: dict[str, int]) -> dict[str, int]:
    """Group skill counts by category."""
    category_totals: Counter = Counter()
    all_skills: dict[str, str] = {}
    for cat, keywords in config.SKILL_CATEGORIES.items():
        for kw in keywords:
            all_skills[kw.lower()] = cat

    for skill, count in skill_counts.items():
        cat = all_skills.get(skill.lower(), "Other")
        category_totals[cat] += count

    return dict(category_totals.most_common())


def process(raw_data: dict) -> dict:
    """
    Process raw collected data into structured analytics.
    Returns analytics dict and saves to processed JSON.
    """
    console.print("[cyan]📊 Processing analytics…[/]")

    curated = raw_data.get("curated_market", {})
    serpapi_jobs = raw_data.get("serpapi_jobs", [])

    # ── Skill Demand ───────────────────────────────────────────────────
    # Start with curated data (always available)
    skill_demand = curated.get("skill_demand", {})

    # Enrich with SerpApi extractions if available
    if serpapi_jobs:
        extracted = _extract_skills_from_descriptions(serpapi_jobs)
        for skill, count in extracted.most_common(50):
            if skill.title() not in skill_demand:
                # find category
                cat = "Other"
                for c, keywords in config.SKILL_CATEGORIES.items():
                    if skill in [k.lower() for k in keywords]:
                        cat = c
                        break
                skill_demand[skill.title()] = {
                    "mentions_pct": round(count / max(len(serpapi_jobs), 1) * 100, 1),
                    "yoy_change": 0,
                    "category": cat,
                    "source": "live_extraction",
                }

    # Sort by mention % descending
    skills_sorted = dict(
        sorted(
            skill_demand.items(),
            key=lambda x: x[1].get("mentions_pct", 0),
            reverse=True,
        )
    )

    # ── Top Skills (flat list for charts) ──────────────────────────────
    top_skills = [
        {"name": name, **data}
        for name, data in list(skills_sorted.items())[:25]
    ]

    # ── Skill Categories for donut chart ───────────────────────────────
    cat_totals: Counter = Counter()
    for name, data in skill_demand.items():
        cat_totals[data.get("category", "Other")] += data.get("mentions_pct", 0)
    skill_categories = [
        {"category": cat, "total_mentions": round(total, 1)}
        for cat, total in cat_totals.most_common()
    ]

    # ── Role Demand ────────────────────────────────────────────────────
    role_demand = curated.get("role_demand", {})
    roles_sorted = sorted(
        [{"role": k, **v} for k, v in role_demand.items()],
        key=lambda x: x.get("postings", 0),
        reverse=True,
    )

    # ── Location Demand ────────────────────────────────────────────────
    location_demand = curated.get("location_demand", {})
    locations_sorted = sorted(
        [{"location": k, **v} for k, v in location_demand.items()],
        key=lambda x: x.get("postings", 0),
        reverse=True,
    )

    # ── Fastest-Growing Skills ─────────────────────────────────────────
    fastest_growing = sorted(
        [{"name": k, **v} for k, v in skill_demand.items()],
        key=lambda x: x.get("yoy_change", 0),
        reverse=True,
    )[:15]

    # ── Emerging Trends ────────────────────────────────────────────────
    emerging_trends = curated.get("emerging_trends", [])

    # ── Market Snapshot ────────────────────────────────────────────────
    market_snapshot = curated.get("market_snapshot", {})

    # ── Salary Analysis ────────────────────────────────────────────────
    salary_data = [
        {"role": k, "avg_salary_usd": v.get("avg_salary_usd", 0)}
        for k, v in role_demand.items()
        if v.get("avg_salary_usd")
    ]
    salary_data.sort(key=lambda x: x["avg_salary_usd"], reverse=True)

    # ── Web Scraping Enrichment ────────────────────────────────────────
    web_data = raw_data.get("web_scraping", {})
    tiobe_rankings = web_data.get("tiobe_index", {}).get("rankings", [])
    indeed_articles = web_data.get("indeed_trends", {}).get("articles", [])
    octoverse_sections = web_data.get("github_octoverse", {}).get("sections", [])

    # ── Compile analytics ──────────────────────────────────────────────
    analytics = {
        "generated_at": datetime.now().isoformat(),
        "market_snapshot": market_snapshot,
        "top_skills": top_skills,
        "skill_categories": skill_categories,
        "fastest_growing_skills": fastest_growing,
        "roles": roles_sorted,
        "locations": locations_sorted,
        "salary_data": salary_data,
        "emerging_trends": emerging_trends,
        "tiobe_rankings": tiobe_rankings,
        "indeed_articles": indeed_articles,
        "octoverse_highlights": octoverse_sections[:5],
        "live_jobs_count": len(serpapi_jobs),
        "data_sources": [
            "Curated Market Intelligence (BLS, LinkedIn, Dice, Gartner)",
        ],
    }

    if serpapi_jobs:
        analytics["data_sources"].append(f"SerpApi Live Jobs ({len(serpapi_jobs)} postings)")
    if tiobe_rankings:
        analytics["data_sources"].append("TIOBE Programming Index")
    if indeed_articles:
        analytics["data_sources"].append("Indeed Hiring Lab")
    if octoverse_sections:
        analytics["data_sources"].append("GitHub Octoverse 2024")

    # Save
    out_path = config.PROCESSED_DIR / "analytics.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(analytics, f, indent=2, ensure_ascii=False)
    console.print(f"[green]✓ Analytics saved → {out_path}[/]")

    return analytics
