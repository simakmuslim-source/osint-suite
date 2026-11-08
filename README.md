# OSINT Suite

**Multifunctional free OSINT toolkit**  
Runs locally. No paid APIs for core features.

## Status

| Module | Status |
|--------|--------|
| Username (Sherlock) | ✅ |
| Phone lookup + VK guidance | ✅ |
| Contacts scraper | ✅ |
| Local reverse image | ✅ |
| Report (Markdown + JSON) | ✅ |
| Courts (sudrf interface) | ✅ guidance |
| **Web UI (Streamlit)** | ✅ |

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
python cli.py court "Иванов Иван" --region Москва --year 2024
python cli.py report --username someuser --phone +7916... --url https://example.com --output report.md --json-output report.json
```

## Web UI

```bash
streamlit run webapp.py
```

Opens a local browser with tabs: Username · Phone · Contacts · Image · Courts · Report.

## GitHub Actions

**Actions → OSINT Report → Run workflow**  
or open an issue with label `osint-request`.

## Notes

- **Photo search** is local perceptual-hash only (near-duplicates in a folder you provide). For face search across the internet use Yandex / search4faces, then feed usernames into Sherlock.
- **Courts** module gives official links and safe guidance; aggressive bulk scraping of sudrf is not enabled by default.

## License

MIT
