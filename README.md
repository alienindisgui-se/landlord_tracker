# landlord_tracker

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

Automated rental property scraper that tracks available apartments across Swedish housing providers.

## About

This project continuously monitors rental listings from multiple Swedish property management sites, normalizes the data into a consistent schema, and produces timestamped reports. It runs automatically on a scheduled cadence so you always have fresh inventory data without manual checks.

## Features

- Multi-source scraping from subo.se, sveafastigheter.se, and neobo.se
- Normalized listing schema with address, rooms, size, rent, and availability
- JSON Schema validation for data integrity
- Automated merge pipeline across sources
- Markdown report generation with scraper health status
- GitHub Actions workflow for scheduled execution

## Quick start

```bash
# Install dependencies
pip install -r requirements.txt

# Run full scrape pipeline
python runners/run_scrapers.py

# Generate markdown report
python runners/generate_report.py

# Validate merged listings against schema
python runners/validate_listings.py
```

## Tech stack

- Python 3.9+
- requests + BeautifulSoup for scraping
- JSON Schema for validation
- GitHub Actions for scheduling

## How it works

1. `run_scrapers.py` loads target sources from `config/scrapers.json`
2. Each source-specific scraper extracts listings and writes raw JSON to `data/`
3. `merge_listings.py` combines all source files into `data/listings.json`
4. `generate_report.py` produces a status report in `report/`
5. Validation ensures every listing matches `schemas/listing.schema.json`

## Contributing

Issues and PRs are welcome. For major changes, open an issue first to discuss the approach.

## License

MIT