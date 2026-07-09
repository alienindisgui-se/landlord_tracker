#!/usr/bin/env python3

import importlib.util
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
    
    # Run all scrapers
    scrapers = ['subo_scraper', 'sveafastigheter_scraper', 'neobo_scraper']
    for scraper_name in scrapers:
        try:
            print(f"\nRunning {scraper_name}...")
            scraper = load_scraper(scraper_name)
            if hasattr(scraper, 'scrape'):
                scraper.scrape()
                print(f"[OK] {scraper_name} completed successfully")
            else:
                print(f"[FAIL] {scraper_name} missing scrape() function")
        except Exception as e:
            print(f"[FAIL] {scraper_name} failed: {e}")
    
    # Merge results
    print("\nMerging listings...")
    merge = load_scraper('merge_listings')
    if hasattr(merge, 'merge_listings'):
        merge.merge_listings()
        print("[OK] Merge completed")
    else:
        print("[FAIL] merge_listings missing merge_listings() function")
    
    print("\nPipeline completed!")

if __name__ == '__main__':
    main()