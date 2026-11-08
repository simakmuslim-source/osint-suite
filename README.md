# OSINT Suite

**Multifunctional free OSINT toolkit**  
Everything runs locally. No paid APIs. No API keys required for core features.

## Status

| Module | Status | Notes |
|--------|--------|-------|
| **Username (Sherlock)** | ✅ Working | 400+ sites |
| **Phone lookup** | ✅ Working | Normalize + operator/region (DEF ranges) |
| **VK OSINT** | ✅ Guidance | Safe free helpers + interface for token later |
| **Local reverse image** | ✅ Working | Perceptual hash |
| Contact scraper | ✅ Basic | Emails + phones from pages |
| Russian courts | ⏳ Planned | sudrf* |
| Web UI | ⏳ Planned | |

## Quick Start

```bash
git clone https://github.com/simakmuslim-source/osint-suite.git
cd osint-suite
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Commands

```bash
# Username search
python cli.py username someuser

# Phone + operator/region
python cli.py phone +79161234567

# Phone + VK guidance
python cli.py phone +79161234567 --vk

# Local reverse image search
python cli.py image photo.jpg --db ./photos --threshold 8

# Full report (Markdown + optional JSON)
python cli.py report --username someuser --phone +7916... --output report.md --json-output report.json
```

### GitHub Actions

**Actions → OSINT Report → Run workflow**  
or open an issue with label `osint-request`.

## Photo search note

`cli.py image` finds **near-duplicate** images in a local folder (perceptual hash).  
It does **not** do internet-wide face recognition. For face search use Yandex / search4faces manually, then feed found usernames into Sherlock.

## License

MIT
