#!/usr/bin/env python3

import importlib.util
import os
import sys
from pathlib import Path

# Add runners directory to path
runners_dir = Path(__file__).parent
sys.path.insert(0, str(runners_dir))

def load_scraper(name):
    spec = importlib.util.spec_from_file_location(name, str(runners_dir / f"{name}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    print("Starting landlord tracker scraper pipeline...")
    
    # Load targets from config
    config_path = runners_dir.parent / "config" / "scrapers.json"
    targets = []
    if config_path.exists():
        import json
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        targets = [t["name"] for t in config.get("targets", [])]
    
    if not targets:
        targets = ['subo', 'sveafastigheter', 'neobo']
    
    statuses = {}
    
    for target_name in targets:
        scraper_name = f"{target_name}_scraper"
        try:
            print(f"\nRunning {scraper_name}...")
            scraper = load_scraper(scraper_name)
            if hasattr(scraper, 'scrape'):
                scraper.scrape()
                statuses[scraper_name] = 'ok'
                print(f"[OK] {scraper_name} completed successfully")
            else:
                statuses[scraper_name] = 'missing_scrape'
                print(f"[FAIL] {scraper_name} missing scrape() function")
        except Exception as e:
            statuses[scraper_name] = f'error: {e}'
            print(f"[FAIL] {scraper_name} failed: {e}")
    
    # Merge results
    print("\nMerging listings...")
    merge = load_scraper('merge_listings')
    if hasattr(merge, 'merge_listings'):
        merge.merge_listings()
        print("[OK] Merge completed")
    else:
        print("[FAIL] merge_listings missing merge_listings() function")
    
    # Enrich with neighborhood summaries (optional, requires GEMINI_API_KEY)
    if os.environ.get('GEMINI_API_KEY'):
        print("\nEnriching listings with neighborhood summaries...")
        try:
            enrich = load_scraper('enrich_neighborhood')
            if hasattr(enrich, 'enrich_neighborhood'):
                enrich.enrich_neighborhood()
                print("[OK] Enrichment completed")
            else:
                print("[SKIP] enrich_neighborhood missing enrich_neighborhood() function")
        except Exception as e:
            print(f"[FAIL] Enrichment failed: {e}")
    else:
        print("\n[Skipping enrichment] GEMINI_API_KEY not set")
    
    # Save statuses for report generation
    import json
    from datetime import datetime
    status_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'statuses': statuses
    }
    with open('data/scrape_status.json', 'w', encoding='utf-8') as f:
        json.dump(status_data, f, indent=2, ensure_ascii=False)
    
    print("\nPipeline completed!")

if __name__ == '__main__':
    main()