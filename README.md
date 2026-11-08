# OSINT Suite

**Multifunctional free OSINT toolkit**  
Local · no paid APIs for core features · MIT

## Features

| Module | Status |
|--------|--------|
| Username search (Sherlock) | OK |
| Phone lookup + VK guidance | OK |
| Contacts scraper | OK |
| Local reverse image (phash) | OK |
| Courts (sudrf links + guidance) | OK |
| Report Markdown / JSON / PDF | OK |
| Web UI (Streamlit) | OK |
| Docker | OK |
| GitHub Actions report | OK |

## Install

```bash
git clone https://github.com/simakmuslim-source/osint-suite.git
cd osint-suite
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## CLI

```bash
python cli.py username someuser
python cli.py phone +79161234567 --vk
python cli.py contacts https://example.com
python cli.py image photo.jpg --db ./photos --threshold 8
python cli.py court "Ivanov" --region Moscow --year 2024

# Full report (MD + JSON + PDF)
python cli.py report \
  --username someuser \
  --phone +7916... \
  --url https://example.com \
  --output report.md \
  --json-output report.json \
  --pdf-output report.pdf
```

## Web UI

```bash
streamlit run webapp.py
```

## Docker

```bash
docker compose up --build
# open http://localhost:8501
```

Or:

```bash
docker build -t osint-suite .
docker run -p 8501:8501 osint-suite
```

## GitHub Actions

Actions → OSINT Report → Run workflow  
or create an issue with label `osint-request`.

## Notes

- Image search is local near-duplicate search only.
- Face search across the internet → use Yandex / search4faces, then Sherlock.
- Courts module gives official links; bulk sudrf scraping is not enabled by default.

## License

MIT
