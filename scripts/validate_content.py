#!/usr/bin/env python3
"""Basic guardrails for public medical Markdown content."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SCAN_PATHS = [
    ROOT / "articles",
    ROOT / "BNCT-100-QA.md",
    ROOT / "IPS-100-QA.md",
    ROOT / "kampo-modernization-buntou",
]

PROHIBITED = {
    "百分百有效": "absolute efficacy claim",
    "100%有效": "absolute efficacy claim",
    "保证治愈": "cure guarantee",
    "彻底治愈": "cure guarantee",
    "癌细胞清零": "cancer-clearance claim",
    "最后希望": "fear-based marketing",
    "零副作用": "absolute safety claim",
    "绝对安全": "absolute safety claim",
    "零成瘤风险": "absolute safety claim",
    "零免疫排斥": "absolute safety claim",
    "只杀死癌细胞": "absolute selectivity claim",
    "绿通名额": "scarcity/urgency marketing",
}

REQUIRED_ARTICLE_FIELDS = [
    "title",
    "slug",
    "category",
    "evidence_stage",
    "published_date",
    "updated_date",
    "reviewed_date",
    "summary",
    "notion_url",
    "primary_sources",
]

URL_RE = re.compile(r"https://[^\s)>]+")
errors = []

def check_text(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for phrase, reason in PROHIBITED.items():
        if phrase in text:
            errors.append(f"{path.relative_to(ROOT)}: prohibited phrase '{phrase}' ({reason})")

def check_article(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{path.relative_to(ROOT)}: missing YAML front matter")
        return
    try:
        front = text.split("---\n", 2)[1]
    except IndexError:
        errors.append(f"{path.relative_to(ROOT)}: malformed YAML front matter")
        return
    for field in REQUIRED_ARTICLE_FIELDS:
        if not re.search(rf"(?m)^{re.escape(field)}\s*:", front):
            errors.append(f"{path.relative_to(ROOT)}: missing field '{field}'")
    if "## 风险提示" not in text:
        errors.append(f"{path.relative_to(ROOT)}: missing risk notice")
    if "## 权威来源" not in text:
        errors.append(f"{path.relative_to(ROOT)}: missing source section")
    if not URL_RE.search(text):
        errors.append(f"{path.relative_to(ROOT)}: no HTTPS source URL found")

for target in SCAN_PATHS:
    if target.is_dir():
        for md in sorted(target.glob("*.md")):
            if md.name in {"README.md", "TEMPLATE.md"}:
                continue
            check_text(md)
            check_article(md)
    elif target.exists():
        check_text(target)

if errors:
    print("Medical content validation failed:")
    for item in errors:
        print(f"- {item}")
    sys.exit(1)

print("Medical content validation passed.")
