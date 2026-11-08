"""
Contact information scraper
Based on ContactInfoScraper + Web-Scraping-using-Python
"""

from typing import List, Dict
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}")

def scrape_contacts(url: str) -> Dict[str, List[str]]:
    """
    Extract emails and phone numbers from a webpage.
    """
    try:
        html = urlopen(url, timeout=10).read().decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html, "lxml")
        text = soup.get_text(" ")
        emails = list(set(EMAIL_REGEX.findall(text)))
        phones = list(set(PHONE_REGEX.findall(text)))
        return {"emails": emails, "phones": phones}
    except Exception as e:
        return {"emails": [], "phones": [], "error": str(e)}
