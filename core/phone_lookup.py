"""
Phone number lookup module (free, no paid APIs)

- Normalizes Russian numbers
- Determines country / operator / region by DEF-code ranges (public data)
- Ready for integration with vkOsint (VK search by phone)
"""

from typing import Dict, Any, Optional
import re


def normalize_phone(phone: str) -> str:
    """Bring phone to +7XXXXXXXXXX format when possible."""
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("8") and len(digits) == 11:
        digits = "7" + digits[1:]
    if digits.startswith("7") and len(digits) == 11:
        return "+" + digits
    if len(digits) == 10:
        return "+7" + digits
    return phone.strip()


# Simplified public DEF ranges (Russia). Not exhaustive, good enough for free OSINT.
OPERATOR_RANGES = [
    # (prefix, operator, region)
    ("900", "Beeline", "Russia"),
    ("901", "Beeline", "Russia"),
    ("902", "Beeline / MTS", "Russia"),
    ("903", "Beeline", "Russia"),
    ("904", "Beeline / Tele2", "Russia"),
    ("905", "Beeline", "Russia"),
    ("906", "Beeline", "Russia"),
    ("908", "MTS", "Russia"),
    ("909", "MTS", "Russia"),
    ("910", "MTS", "Russia"),
    ("911", "MTS", "Russia"),
    ("912", "MTS", "Russia"),
    ("913", "MTS", "Siberia"),
    ("914", "MTS", "Far East"),
    ("915", "MTS", "Russia"),
    ("916", "MTS", "Moscow"),
    ("917", "MTS", "Russia"),
    ("918", "MTS", "South"),
    ("919", "MTS", "Russia"),
    ("920", "Megafon", "Russia"),
    ("921", "Megafon", "North-West"),
    ("922", "Megafon", "Urals"),
    ("923", "Megafon", "Siberia"),
    ("924", "Megafon", "Far East"),
    ("925", "Megafon", "Moscow"),
    ("926", "Megafon", "Moscow"),
    ("927", "Megafon", "Volga"),
    ("928", "Megafon", "South"),
    ("929", "Megafon", "Russia"),
    ("930", "Megafon", "Russia"),
    ("931", "Megafon", "North-West"),
    ("932", "Megafon", "Urals"),
    ("933", "Megafon", "Siberia"),
    ("934", "Megafon", "Far East"),
    ("936", "Beeline", "Russia"),
    ("937", "Beeline", "Russia"),
    ("938", "Beeline", "South"),
    ("950", "Tele2", "Russia"),
    ("951", "Tele2", "Russia"),
    ("952", "Tele2", "Russia"),
    ("953", "Tele2", "Russia"),
    ("958", "Tele2", "Russia"),
    ("960", "Beeline", "Russia"),
    ("961", "Beeline", "Russia"),
    ("962", "Beeline", "Russia"),
    ("963", "Beeline", "Russia"),
    ("964", "Beeline", "Russia"),
    ("965", "Beeline", "Russia"),
    ("966", "Beeline", "Russia"),
    ("967", "Beeline", "Russia"),
    ("968", "Beeline", "Russia"),
    ("969", "Beeline", "Russia"),
    ("977", "Yota / Megafon", "Russia"),
    ("978", "Crimea / local", "Crimea"),
    ("980", "MTS", "Russia"),
    ("981", "MTS", "North-West"),
    ("982", "MTS", "Urals"),
    ("983", "MTS", "Siberia"),
    ("984", "MTS", "Far East"),
    ("985", "MTS", "Moscow"),
    ("986", "MTS", "Russia"),
    ("987", "MTS", "Volga"),
    ("988", "MTS", "South"),
    ("989", "MTS", "Russia"),
    ("999", "Yota / Beeline", "Russia"),
]


def _guess_operator(normalized: str) -> Dict[str, Optional[str]]:
    if not normalized.startswith("+7") or len(normalized) != 12:
        return {"operator": None, "region": None, "country": None}

    prefix = normalized[2:5]  # three digits after +7
    for p, operator, region in OPERATOR_RANGES:
        if prefix == p:
            return {
                "operator": operator,
                "region": region,
                "country": "Russia",
            }
    return {
        "operator": "Unknown (RU mobile)",
        "region": "Russia",
        "country": "Russia",
    }


def lookup_phone(phone: str) -> Dict[str, Any]:
    """
    Free phone lookup.

    Returns structured dict with normalized number, operator, region,
    and placeholders for VK accounts (to be filled by vk_osint module).
    """
    normalized = normalize_phone(phone)
    info = _guess_operator(normalized)

    return {
        "input": phone,
        "normalized": normalized,
        "country": info["country"],
        "operator": info["operator"],
        "region": info["region"],
        "vk_accounts": [],          # filled later by core.vk_osint
        "notes": "Free heuristic lookup (DEF ranges). No paid APIs used.",
        "sources": ["public DEF code ranges"],
    }
