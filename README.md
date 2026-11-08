# OSINT Suite

**Multifunctional free OSINT toolkit** combining the best tools from starred repositories:

- **Username search** → Sherlock
- **Phone lookup** → Gokboru_Intel + vkOsint
- **Reverse image / face search** → image-match + perceptual hash
- **VK OSINT** → OSINTvk / vk-osint-en
- **Contact extraction** → ContactInfoScraper
- **Russian courts** → sudrfparser / sudrfscraper
- **Web scraping** → emails & phones

## Quick Start

```bash
git clone https://github.com/simakmuslim-source/osint-suite.git
cd osint-suite
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### CLI Usage

```bash
# Username search
python cli.py username ivanov

# Phone lookup
python cli.py phone +79161234567

# Reverse image search (local perceptual hash)
python cli.py image path/to/photo.jpg

# Full report (username + phone + image)
python cli.py report --username ivanov --phone +7916... --image photo.jpg --output report.md
```

### GitHub Actions

Trigger a report generation via `workflow_dispatch` or by creating an issue with the label `osint-request`.

The workflow produces a Markdown + JSON report as an artifact.

## Modules

| Module | Source | Status |
|--------|--------|--------|
| `core/username_search.py` | Sherlock | Ready (wrapper) |
| `core/phone_lookup.py` | Gokboru + vkOsint | Stub |
| `core/reverse_image.py` | image-match | Stub |
| `core/vk_osint.py` | OSINTvk | Stub |
| `core/contact_scraper.py` | ContactInfoScraper | Stub |
| `core/court_search.py` | sudrf* | Stub |

## Roadmap

- [x] Repository structure
- [x] CLI skeleton
- [x] GitHub Actions workflow
- [ ] Full integration of Sherlock
- [ ] Phone + VK modules
- [ ] Local reverse image with perceptual hashing
- [ ] Report generator (MD + JSON + optional PDF)
- [ ] Web UI / Telegram bot later

## License

MIT
