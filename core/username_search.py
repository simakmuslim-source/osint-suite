"""
Username search module – wrapper around Sherlock
"""

from typing import List, Dict

def search_username(username: str) -> List[Dict]:
    """
    Search for a username across social networks.
    Currently a stub – will call Sherlock.
    """
    # TODO: integrate sherlock-project/sherlock
    # Example:
    # from sherlock_project import sherlock
    # results = sherlock(username)
    return [
        {"site": "example.com", "url": f"https://example.com/{username}", "exists": False}
    ]
