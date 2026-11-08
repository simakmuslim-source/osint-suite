# OSINT Suite

**Multifunctional free OSINT toolkit**  
Runs locally. No paid APIs for core features.

## Status

| Module | Status | Notes |
|--------|--------|-------|
| Username (Sherlock) | ✅ | 400+ sites |
| Phone lookup | ✅ | Operator + region (DEF) |
| VK OSINT | ✅ | Safe guidance + token-ready interface |
| Contacts scraper | ✅ | Emails, phones, social links from URL |
| Local reverse image | ✅ | Perceptual hash |
| Report generator | ✅ | Markdown + JSON |
| Russian courts | ⏳ | Interface ready, scraping not enabled |
| Web UI | ⏳ | Planned |

## Install

```bash
git clone https://github.com/simakmuslim-source/osint-suite.git
cd osint-suite
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Commands

```bash
# Username
python cli.py username someuser

# Phone + VK tips
python cli.py phone +79161234567 --vk

# Contacts from webpage
python cli.py contacts https://example.com

# Local similar images
python cli.py image photo.jpg --db ./photos --threshold 8

# Full report
python cli.py report \
  --username someuser \
  --phone +7916... \
  --url https://example.com \
  --output report.md \
  --json-output report.json
```

## GitHub Actions

**Actions → OSINT Report → Run workflow**  
or open an issue with label `osint-request`.

## Photo search note

`cli.py image` finds near-duplicates in a **local folder**.  
It does not do internet face recognition. For faces use Yandex / search4faces, then feed usernames into Sherlock.

## License

MIT
