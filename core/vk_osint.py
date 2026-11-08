"""
VK OSINT helpers

Note: Full automatic search of VK accounts by phone usually requires
either official VK API (with token) or third-party tools that may
violate ToS. Here we provide:

1. Clean interface ready for vkOsint / similar packages
2. Free helpers that do not break the law / ToS aggressively
3. Manual investigation tips
"""

from typing import List, Dict, Any, Optional
from .phone_lookup import normalize_phone, lookup_phone


def search_vk_by_phone(phone: str, token: Optional[str] = None) -> Dict[str, Any]:
    """
    Attempt to find VK accounts linked to a phone number.

    Without a VK access token this returns structured guidance
    and the normalized phone instead of scraping.
    """
    normalized = normalize_phone(phone)
    base = lookup_phone(normalized)

    result = {
        "phone": normalized,
        "operator": base.get("operator"),
        "region": base.get("region"),
        "accounts": [],
        "method": None,
        "notes": [],
    }

    if token:
        result["notes"].append(
            "VK token provided — implement official users.get / account search here."
        )
        result["method"] = "vk_api_token"
        # Placeholder for future official API integration
    else:
        result["method"] = "manual_guidance"
        result["notes"].extend([
            "Automatic bulk phone→VK search without token is restricted.",
            "Recommended free manual steps:",
            "1. Try the phone in VK password recovery (do not submit).",
            "2. Search the number in Google/Yandex with site:vk.com",
            "3. Check public people-search services that aggregate open data.",
            "4. If you have a legitimate VK token — pass it to this function later.",
        ])

    return result


def format_vk_result(data: Dict[str, Any]) -> str:
    """Pretty text for CLI / report."""
    lines = [
        f"Phone: {data.get('phone')}",
        f"Operator: {data.get('operator')} ({data.get('region')})",
        f"Method: {data.get('method')}",
        "",
    ]
    if data.get("accounts"):
        lines.append("Found accounts:")
        for acc in data["accounts"]:
            lines.append(f"  - {acc}")
    else:
        lines.append("No accounts returned automatically.")
    if data.get("notes"):
        lines.append("\nNotes:")
        for n in data["notes"]:
            lines.append(f"  • {n}")
    return "\n".join(lines)
