#!/usr/bin/env python3
"""Generate markdown report from listings.json and scrape_status.json"""
import json
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LISTINGS_PATH = REPO / "data" / "listings.json"
STATUS_PATH = REPO / "data" / "scrape_status.json"
REPORT_DIR = REPO / "report"

def generate_report():
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = REPORT_DIR / f"{today}.md"
    
    listings = []
    if LISTINGS_PATH.exists():
        with open(LISTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            listings = data.get("listings", [])
    
    statuses = {}
    if STATUS_PATH.exists():
        with open(STATUS_PATH, "r", encoding="utf-8") as f:
            statuses = json.load(f).get("statuses", {})
    
    # Count listings per source
    counts = {}
    for listing in listings:
        source = listing.get("source", "unknown")
        counts[source] = counts.get(source, 0) + 1
    
    # Determine status for each target scraper from config
    config_path = REPO / "config" / "scrapers.json"
    targets = []
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        targets = [f"{t['name']}_scraper" for t in config.get("targets", [])]
    
    if not targets:
        targets = ["subo_scraper", "sveafastigheter_scraper", "neobo_scraper"]
    
    rows = []
    for target in targets:
        name = target.replace("_scraper", "").capitalize()
        status = "✅"
        if target in statuses and statuses[target] != "ok":
            status = "⚠️"
        elif counts.get(name.lower(), 0) == 0:
            status = "❌"
        rows.append(f"| {name} | {status} |")
    
    report = f"# Scraper Report - {today}\n\n"
    report += "| Landlord | Status |\n"
    report += "| --- | --- |\n"
    report += "\n".join(rows)
    report += "\n"
    
    REPORT_DIR.mkdir(exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"Generated report: {report_path}")

if __name__ == "__main__":
    generate_report()
