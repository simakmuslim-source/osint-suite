# OSINT Suite

**Multifunctional free OSINT toolkit** combining the best tools from starred repositories.

Everything is **100% free** and runs locally. No API keys, no paid requests.

## Features

| Module | Status | Notes |
|--------|--------|-------|
| **Username search (Sherlock)** | ✅ Working | 400+ sites, free, no keys |
| **Local reverse image** | ✅ Working | Perceptual hash (imagehash) |
| Phone lookup | ⏳ Stub | Gokboru + vkOsint planned |
| VK OSINT | ⏳ Stub | |
| Contact scraper | ✅ Basic | Emails + phones from pages |
| Russian courts | ⏳ Stub | sudrf* |

## Quick Start

```bash
git clone https://github.com/simakmuslim-source/osint-suite.git
cd osint-suite
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### CLI Usage

```bash
# Username search (Sherlock)
python cli.py username someuser

# Local reverse image search
python cli.py image path/to/photo.jpg --db ./photos --threshold 8

# Phone (stub for now)
python cli.py phone +79161234567

# Full report
python cli.py report --username someuser --output report.md
```

### GitHub Actions

Go to **Actions → OSINT Report → Run workflow**.  
You can also open an issue with the label `osint-request`.

The workflow uploads a Markdown report as an artifact.

## Important notes about photo search

- `cli.py image` does **local** perceptual-hash search (finds near-duplicates in a folder you provide).
- It does **not** do face recognition across the internet (PimEyes / Yandex style).
- For real face search use Yandex Images / search4faces / etc. manually, then feed interesting usernames back into Sherlock.

## License

MIT
