"""
Configuration for the Tech Job Trends Agent.
"""
import os
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure directories exist
for d in [RAW_DIR, PROCESSED_DIR, TEMPLATES_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── API Keys ───────────────────────────────────────────────────────────────
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")

# ── Search Configuration ───────────────────────────────────────────────────
TARGET_ROLES = [
    "Software Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
    "DevOps Engineer",
    "Cloud Architect",
    "Cybersecurity Analyst",
    "Full Stack Developer",
    "AI Engineer",
    "Data Engineer",
    "Platform Engineer",
    "Site Reliability Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Product Manager Technical",
    "Solutions Architect",
]

TARGET_LOCATIONS = [
    "United States",
    "Canada",
    "New York, NY",
    "San Francisco, CA",
    "Seattle, WA",
    "Austin, TX",
    "Toronto, Canada",
    "Vancouver, Canada",
    "Chicago, IL",
    "Boston, MA",
    "Denver, CO",
    "Atlanta, GA",
    "Waterloo, Canada",
    "Los Angeles, CA",
    "Dallas, TX",
    "Miami, FL",
    "Washington, DC",
    "Montreal, Canada",
]

# ── Skill Categories ──────────────────────────────────────────────────────
SKILL_CATEGORIES = {
    "AI / Machine Learning": [
        "machine learning", "deep learning", "neural network", "nlp",
        "natural language processing", "computer vision", "tensorflow",
        "pytorch", "llm", "large language model", "generative ai",
        "gen ai", "transformers", "reinforcement learning", "mlops",
        "model training", "fine-tuning", "prompt engineering",
        "langchain", "hugging face", "openai", "ai agent",
    ],
    "Cloud & Infrastructure": [
        "aws", "azure", "gcp", "google cloud", "cloud", "ec2", "s3",
        "lambda", "cloudformation", "terraform", "pulumi", "ansible",
        "infrastructure as code", "iac", "serverless", "cloud native",
    ],
    "Data Engineering": [
        "sql", "nosql", "postgresql", "mysql", "mongodb", "redis",
        "kafka", "spark", "airflow", "etl", "data pipeline",
        "data warehouse", "snowflake", "databricks", "dbt",
        "big data", "hadoop", "data lake", "delta lake",
    ],
    "DevOps & SRE": [
        "docker", "kubernetes", "k8s", "ci/cd", "jenkins", "github actions",
        "gitlab ci", "helm", "prometheus", "grafana", "datadog",
        "observability", "monitoring", "sre", "site reliability",
        "argocd", "istio", "service mesh",
    ],
    "Cybersecurity": [
        "cybersecurity", "security", "penetration testing", "soc",
        "siem", "threat detection", "vulnerability", "encryption",
        "zero trust", "identity management", "iam", "compliance",
        "devsecops", "owasp", "firewall", "intrusion detection",
    ],
    "Web & Mobile Development": [
        "react", "angular", "vue", "next.js", "node.js", "typescript",
        "javascript", "html", "css", "tailwind", "graphql", "rest api",
        "swift", "kotlin", "flutter", "react native", "svelte",
    ],
    "Programming Languages": [
        "python", "java", "go", "golang", "rust", "c++", "c#",
        "scala", "ruby", "php", "elixir", "zig",
    ],
    "Soft Skills & Methodology": [
        "agile", "scrum", "leadership", "communication",
        "problem solving", "collaboration", "mentoring",
        "system design", "architecture", "technical writing",
    ],
}

# ── Trend Data Sources (public URLs for scraping) ─────────────────────────
TREND_SOURCES = [
    {
        "name": "Indeed Hiring Lab",
        "url": "https://www.hiringlab.org/",
        "type": "report",
    },
    {
        "name": "Stack Overflow Survey",
        "url": "https://survey.stackoverflow.co/2024/",
        "type": "survey",
    },
    {
        "name": "GitHub Octoverse",
        "url": "https://github.blog/news-insights/octoverse/octoverse-2024/",
        "type": "report",
    },
    {
        "name": "TIOBE Index",
        "url": "https://www.tiobe.com/tiobe-index/",
        "type": "ranking",
    },
]
