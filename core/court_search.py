"""
Russian courts (sudrf) search interface

Provides structured guidance and ready-made search URLs.
Does not perform aggressive bulk scraping by default.
"""

from typing import Dict, Any, Optional
from urllib.parse import quote


def search_cases(
    query: str,
    region: Optional[str] = None,
    year: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Build court-search guidance and direct links for a query.
    """
    q = quote(query)
    links = [
        {
            "name": "ГАС Правосудие (поиск)",
            "url": f"https://bsr.sudrf.ru/bigs/portal.html",
        },
        {
            "name": "sudrf.ru",
            "url": "https://sudrf.ru",
        },
        {
            "name": "Мосгорсуд",
            "url": "https://mos-gorsud.ru",
        },
        {
            "name": "Google site:sudrf.ru",
            "url": f"https://www.google.com/search?q=site:sudrf.ru+{q}",
        },
        {
            "name": "Yandex site:sudrf.ru",
            "url": f"https://yandex.ru/search/?text=site:sudrf.ru+{q}",
        },
    ]

    if region:
        links.append(
            {
                "name": f"Search with region hint ({region})",
                "url": f"https://www.google.com/search?q=site:sudrf.ru+{q}+{quote(region)}",
            }
        )

    notes = [
        "Bulk automated scraping of sudrf.ru may violate ToS and trigger blocks.",
        "Prefer official portals and manual verification of case cards.",
        "For automation later: integrate sudrfparser/sudrfscraper with delays + cache.",
    ]
    if year:
        notes.append(f"Filter manually by year: {year}")

    return {
        "query": query,
        "region": region,
        "year": year,
        "cases": [],
        "status": "guidance",
        "links": links,
        "suggested_urls": [x["url"] for x in links],
        "notes": notes,
    }


def format_court_result(data: Dict[str, Any]) -> str:
    lines = [
        f"Query: {data.get('query')}",
        f"Region: {data.get('region') or '—'}",
        f"Year: {data.get('year') or '—'}",
        f"Status: {data.get('status')}",
        "",
    ]
    if data.get("links"):
        lines.append("Direct links:")
        for item in data["links"]:
            lines.append(f"  • {item['name']}: {item['url']}")
    if data.get("notes"):
        lines.append("\nNotes:")
        for n in data["notes"]:
            lines.append(f"  • {n}")
    return "\n".join(lines)
