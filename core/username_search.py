"""
Username search module – wrapper around Sherlock (sherlock-project)
Free, open-source, no API keys required.
"""

from typing import List, Dict
import subprocess
import json
import tempfile
from pathlib import Path


def search_username(username: str, timeout: int = 120) -> List[Dict]:
    """
    Search for a username across social networks using Sherlock.

    Returns list of dicts:
    [
        {"site": "GitHub", "url": "https://github.com/username", "exists": True},
        ...
    ]
    """
    results = []

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / f"{username}.json"

            # Run Sherlock and ask for JSON output
            cmd = [
                "sherlock",
                username,
                "--json",
                str(output_file),
                "--print-found",
                "--timeout",
                "15",
                "--no-color",
            ]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            # Sherlock writes results to the json file
            if output_file.exists():
                data = json.loads(output_file.read_text(encoding="utf-8"))
                # Sherlock JSON format is usually { "site": {"url_user": ..., "status": ...}, ... }
                for site, info in data.items():
                    if isinstance(info, dict):
                        status = str(info.get("status", "")).lower()
                        exists = "claimed" in status or status == "found" or info.get("http_status") == 200
                        url = info.get("url_user") or info.get("url") or f"https://{site}/{username}"
                        results.append({
                            "site": site,
                            "url": url,
                            "exists": exists,
                            "status": info.get("status"),
                        })
            else:
                # Fallback: parse stdout if json not produced
                for line in proc.stdout.splitlines():
                    if "http" in line.lower() and username in line:
                        results.append({
                            "site": "unknown",
                            "url": line.strip(),
                            "exists": True,
                        })

    except FileNotFoundError:
        results.append({
            "site": "error",
            "url": "",
            "exists": False,
            "status": "Sherlock not installed. Run: pip install sherlock-project",
        })
    except subprocess.TimeoutExpired:
        results.append({
            "site": "error",
            "url": "",
            "exists": False,
            "status": f"Timeout after {timeout}s",
        })
    except Exception as e:
        results.append({
            "site": "error",
            "url": "",
            "exists": False,
            "status": str(e),
        })

    return results
