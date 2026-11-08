"""
Russian courts (sudrf) search interface

Placeholder ready for integration with sudrfparser / sudrfscraper.
Does not scrape courts yet — only provides a clean API and guidance.
"""

from typing import Dict, Any, List, Optional


def search_cases(
    query: str,
    region: Optional[str] = None,
    year: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Search court cases by name / case number / party.

    Currently returns structured guidance. Later will call sudrf modules.
    """
    return {
        "query": query,
        "region": region,
        "year": year,
        "cases": [],
        "status": "not_implemented",
        "notes": [
            "Automatic bulk scraping of sudrf.ru can violate ToS and rate limits.",
            "Recommended free approaches:",
            "1. Use official court websites / GAS Pravosudie manually.",
            "2. Integrate sudrfparser / sudrfscraper carefully with delays and caching.",
            "3. For production — prefer official APIs or paid legal databases.",
        ],
        "suggested_urls": [
            "https://sudrf.ru",
            "https://bsr.sudrf.ru/bigs/portal.html",
            "https://mos-gorsud.ru",
        ],
    }


def format_court_result(data: Dict[str, Any]) -> str:
    lines = [
        f"Query: {data.get('query')}",
        f"Region: {data.get('region') or '—'}",
        f"Year: {data.get('year') or '—'}",
        f"Status: {data.get('status')}",
        "",
    ]
    if data.get("cases"):
        lines.append("Cases:")
        for c in data["cases"]:
            lines.append(f"  - {c}")
    else:
        lines.append("No cases returned (module not fully implemented yet).")
    if data.get("notes"):
        lines.append("\nNotes:")
        for n in data["notes"]:
            lines.append(f"  • {n}")
    return "\n".join(lines)
