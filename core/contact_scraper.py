"""
Contact information scraper
Based on ContactInfoScraper + Web-Scraping-using-Python
"""

from typing import Dict, List, Any
import re
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(
    r"(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"
)

SOCIAL_PATTERNS = {
    "vk": re.compile(r"https?://(?:www\.)?vk\.com/[\w./-]+", re.I),
    "telegram": re.compile(r"https?://(?:t\.me|telegram\.me)/[\w]+", re.I),
    "instagram": re.compile(r"https?://(?:www\.)?instagram\.com/[\w./]+", re.I),
    "facebook": re.compile(r"https?://(?:www\.)?facebook\.com/[\w./]+", re.I),
    "ok": re.compile(r"https?://(?:www\.)?ok\.ru/[\w./]+", re.I),
}

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def scrape_contacts(url: str, timeout: int = 12) -> Dict[str, Any]:
    """
    Extract emails, phones and social links from a webpage.
    """
    result: Dict[str, Any] = {
        "url": url,
        "emails": [],
        "phones": [],
        "social": {},
        "error": None,
    }

    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        soup = BeautifulSoup(html, "lxml")
        text = soup.get_text(" ")

        # Also check mailto: and tel: links
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("mailto:"):
                text += " " + href[7:]
            elif href.startswith("tel:"):
                text += " " + href[4:]

        emails = sorted(set(EMAIL_REGEX.findall(text)))
        phones = sorted(set(PHONE_REGEX.findall(text)))

        social = {}
        for name, pattern in SOCIAL_PATTERNS.items():
            found = sorted(set(pattern.findall(html)))
            if found:
                social[name] = found

        result["emails"] = emails
        result["phones"] = phones
        result["social"] = social

    except (URLError, HTTPError, TimeoutError) as e:
        result["error"] = str(e)
    except Exception as e:
        result["error"] = str(e)

    return result
