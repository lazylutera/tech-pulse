"""
Career insights module — generates actionable short-term and long-term
recommendations based on analytics data.
"""
from datetime import datetime

from rich.console import Console

console = Console()


def generate(analytics: dict) -> dict:
    """
    Generate career insights from processed analytics.
    Returns structured insights for the dashboard.
    """
    console.print("[cyan]🔮 Generating career insights…[/]")

    top_skills = analytics.get("top_skills", [])
    fastest = analytics.get("fastest_growing_skills", [])
    roles = analytics.get("roles", [])
    emerging = analytics.get("emerging_trends", [])
    salary_data = analytics.get("salary_data", [])

    # ── Short-term (6-12 months) ───────────────────────────────────────
    short_term_skills = []
    for s in top_skills[:10]:
        short_term_skills.append({
            "skill": s["name"],
            "demand_pct": s.get("mentions_pct", 0),
            "category": s.get("category", ""),
            "reason": f"Mentioned in {s.get('mentions_pct', 0)}% of tech postings — high immediate demand",
        })

    top_growth_roles = [r for r in roles if r.get("yoy_change", 0) > 15][:5]
    short_term_roles = []
    for r in top_growth_roles:
        short_term_roles.append({
            "role": r["role"],
            "postings": r.get("postings", 0),
            "growth": f"{r.get('yoy_change', 0)}% YoY",
            "salary": f"${r.get('avg_salary_usd', 0):,}",
            "reason": f"Strong hiring momentum with {r.get('yoy_change', 0)}% year-over-year growth",
        })

    short_term = {
        "title": "Short-Term Priorities (6-12 Months)",
        "summary": (
            "Focus on skills with the highest current demand to maximize "
            "immediate employability and negotiating power."
        ),
        "skills": short_term_skills,
        "hot_roles": short_term_roles,
        "action_items": [
            {
                "action": "Build AI/ML proficiency",
                "detail": "LLMs and GenAI are in nearly 40% of job listings. Start with prompt engineering, then move to fine-tuning and RAG architectures.",
                "urgency": "High",
            },
            {
                "action": "Get cloud-certified",
                "detail": "AWS, Azure, or GCP certifications appear in 45%+ of postings. AWS Solutions Architect or Azure AI Engineer are high-ROI certifications.",
                "urgency": "High",
            },
            {
                "action": "Master containerization",
                "detail": "Docker (52%) and Kubernetes (40%) are baseline expectations for backend and infra roles.",
                "urgency": "Medium",
            },
            {
                "action": "Strengthen system design skills",
                "detail": "System design is a top interview filter and critical for senior-level roles paying $160K+.",
                "urgency": "Medium",
            },
            {
                "action": "Add TypeScript to your toolkit",
                "detail": "TypeScript has surpassed JavaScript in demand growth (15% YoY) and is expected in full-stack and frontend roles.",
                "urgency": "Medium",
            },
        ],
    }

    # ── Long-term (2-5 years) ──────────────────────────────────────────
    long_term_skills = []
    for s in fastest[:10]:
        if s.get("yoy_change", 0) > 20:
            long_term_skills.append({
                "skill": s["name"],
                "growth": f"{s.get('yoy_change', 0)}% YoY",
                "category": s.get("category", ""),
                "reason": f"Exceptional growth trajectory — investing now yields compound career returns",
            })

    long_term_trends = []
    for t in emerging:
        long_term_trends.append({
            "trend": t["trend"],
            "growth": t.get("growth", ""),
            "maturity": t.get("maturity", ""),
            "implication": _trend_implication(t["trend"]),
        })

    long_term = {
        "title": "Long-Term Strategy (2-5 Years)",
        "summary": (
            "Invest in skills at the growth frontier. These technologies are "
            "transitioning from early adoption to mainstream — mastering them "
            "now positions you as a leader, not a follower."
        ),
        "skills": long_term_skills,
        "emerging_trends": long_term_trends,
        "action_items": [
            {
                "action": "Become an AI-native engineer",
                "detail": "AI Agents, autonomous systems, and multi-modal AI are the next wave. Learn to build, deploy, and orchestrate AI agent systems.",
                "urgency": "Strategic",
            },
            {
                "action": "Learn Rust or Go as a second systems language",
                "detail": "Rust (28% YoY growth) and Go (18%) are replacing C++ in performance-critical systems, infrastructure, and blockchain.",
                "urgency": "Strategic",
            },
            {
                "action": "Develop platform engineering expertise",
                "detail": "Platform Engineering (31% YoY) is the evolution of DevOps. Internal developer platforms are becoming standard at scale.",
                "urgency": "Strategic",
            },
            {
                "action": "Invest in cybersecurity knowledge",
                "detail": "Zero Trust (40% YoY) and DevSecOps (30% YoY) are non-negotiable as AI-enabled threats proliferate.",
                "urgency": "Strategic",
            },
            {
                "action": "Build cross-functional leadership skills",
                "detail": "Technical Product Management and Solutions Architecture roles are growing steadily and command $158K-$170K salaries.",
                "urgency": "Ongoing",
            },
            {
                "action": "Explore quantum computing fundamentals",
                "detail": "Still early (45% growth from a small base), but enterprises are building quantum-readiness teams. Early movers will have a rare advantage.",
                "urgency": "Exploratory",
            },
        ],
    }

    # ── Skill Gap Radar Data ───────────────────────────────────────────
    # This feeds a radar chart comparing current demand vs. growth potential
    categories = {}
    for s in top_skills:
        cat = s.get("category", "Other")
        if cat not in categories:
            categories[cat] = {"demand": 0, "growth": 0, "count": 0}
        categories[cat]["demand"] += s.get("mentions_pct", 0)
        categories[cat]["growth"] += abs(s.get("yoy_change", 0))
        categories[cat]["count"] += 1

    radar_data = []
    for cat, vals in categories.items():
        n = max(vals["count"], 1)
        radar_data.append({
            "category": cat,
            "current_demand": round(vals["demand"] / n, 1),
            "growth_potential": round(vals["growth"] / n, 1),
        })

    # ── Salary Insights ────────────────────────────────────────────────
    salary_insights = []
    if salary_data:
        top_paying = salary_data[:5]
        for s in top_paying:
            salary_insights.append({
                "role": s["role"],
                "avg_salary": f"${s['avg_salary_usd']:,}",
            })

    insights = {
        "generated_at": datetime.now().isoformat(),
        "short_term": short_term,
        "long_term": long_term,
        "radar_data": radar_data,
        "salary_insights": salary_insights,
        "career_paths": _generate_career_paths(),
    }

    console.print("[green]✓ Career insights generated[/]")
    return insights


def _trend_implication(trend: str) -> str:
    """Return a career implication for a named trend."""
    implications = {
        "AI Agents & Autonomous Systems": "Engineers who can design and orchestrate multi-agent systems will be among the most sought-after in tech.",
        "LLM Fine-tuning & RAG": "Retrieval-Augmented Generation is becoming the standard architecture for enterprise AI — learn vector DBs and embedding pipelines.",
        "Platform Engineering": "The evolution of DevOps into standardized, self-service internal platforms. High demand at companies with 200+ engineers.",
        "Prompt Engineering": "While commoditizing at the basic level, advanced prompt engineering for complex chains and agent workflows remains valuable.",
        "Zero Trust Security": "Every organization is migrating to Zero Trust. Security expertise paired with cloud skills is a premium combination.",
        "Edge AI / TinyML": "As AI moves to devices, engineers who can optimize models for edge deployment will fill a critical skill gap.",
        "Rust for Systems Programming": "Rust's memory safety guarantees are making it the default for new infrastructure, OS-level, and performance-critical code.",
        "Sustainability / Green Tech": "ESG-driven tech hiring is accelerating. Carbon-aware computing and energy-efficient ML training are emerging specializations.",
        "Quantum Computing Readiness": "Quantum-safe cryptography and hybrid quantum-classical algorithms will need specialists as hardware matures.",
        "Multimodal AI": "AI systems that process text, image, audio, and video together are the frontier — expect explosive demand as models improve.",
    }
    return implications.get(trend, "Emerging area with significant growth potential — early expertise gives a strategic advantage.")


def _generate_career_paths() -> list[dict]:
    """Generate recommended career progression paths."""
    return [
        {
            "path": "AI / ML Engineering",
            "stages": [
                "Python + Data Fundamentals → ML Basics (scikit-learn) → Deep Learning (PyTorch) → LLM/GenAI → AI Agents & Autonomous Systems",
            ],
            "target_roles": ["ML Engineer", "AI Engineer", "AI Research Engineer"],
            "salary_range": "$145K — $200K+",
            "demand_signal": "Fastest growing domain (45% YoY for AI Engineer)",
        },
        {
            "path": "Cloud & Platform Engineering",
            "stages": [
                "Linux + Networking → Docker/K8s → Cloud (AWS/Azure/GCP) → IaC (Terraform) → Platform Engineering → SRE",
            ],
            "target_roles": ["Cloud Architect", "Platform Engineer", "SRE"],
            "salary_range": "$148K — $175K",
            "demand_signal": "Steady high demand with strong growth in Platform Engineering (31% YoY)",
        },
        {
            "path": "Data Engineering → Analytics",
            "stages": [
                "SQL + Python → ETL/Airflow → Spark/Kafka → Data Warehouse (Snowflake/Databricks) → dbt + Analytics Engineering",
            ],
            "target_roles": ["Data Engineer", "Analytics Engineer", "Data Architect"],
            "salary_range": "$140K — $170K",
            "demand_signal": "Consistent demand (18.7% YoY) as every company becomes data-driven",
        },
        {
            "path": "Cybersecurity",
            "stages": [
                "Networking + Linux → Security Fundamentals → Cloud Security → DevSecOps → Zero Trust Architecture → Security Architecture",
            ],
            "target_roles": ["Cybersecurity Analyst", "Security Engineer", "CISO"],
            "salary_range": "$130K — $180K+",
            "demand_signal": "Critical shortage — 22% YoY growth driven by AI-enabled threats",
        },
        {
            "path": "Full-Stack → Technical Leadership",
            "stages": [
                "Frontend (React/TS) → Backend (Node/Python/Go) → System Design → Tech Lead → Solutions Architect / Engineering Manager",
            ],
            "target_roles": ["Solutions Architect", "Technical PM", "Engineering Manager"],
            "salary_range": "$150K — $185K",
            "demand_signal": "Evergreen path — system design + leadership skills command premium salaries",
        },
    ]
