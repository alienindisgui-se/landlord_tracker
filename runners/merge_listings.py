#!/usr/bin/env python3

import json
from datetime import datetime
from pathlib import Path

def merge_listings():
    data_dir = Path('data')
    now = datetime.utcnow().isoformat()
    
    # Load existing merged listings if exists
    existing = {}
    listings_path = data_dir / 'listings.json'
    if listings_path.exists():
        with open(listings_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            for item in existing_data.get('listings', []):
                key = (item.get('id', ''), item.get('source', ''))
                existing[key] = item
    
    # Load current scraped data
    sources = ['subo', 'sveafastigheter', 'neobo']
    current_ids = set()
    
    for source in sources:
        src_file = data_dir / f'{source}_listings.json'
        if not src_file.exists():
            continue
        with open(src_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for prop in data.get('properties', []):
                key = (prop.get('id', ''), source)
                current_ids.add(key)
                if key in existing:
                    # Update existing entry
                    existing[key].update(prop)
                    existing[key]['status'] = 'active'
                    existing[key]['last_seen'] = now
                    # Preserve first_seen and deleted_at if already set
                    if 'first_seen' not in existing[key] or existing[key]['first_seen'] is None:
                        existing[key]['first_seen'] = now
                else:
                    # New entry
                    new_entry = dict(prop)
                    new_entry['status'] = 'active'
                    new_entry['first_seen'] = now
                    new_entry['last_seen'] = now
                    new_entry['deleted_at'] = None
                    existing[key] = new_entry
    
    # Mark listings not found in current scrape as deleted
    for key, item in existing.items():
        if item.get('status') != 'deleted' and key not in current_ids:
            item['status'] = 'deleted'
            item['deleted_at'] = now
    
    # Build final output preserving only unique entries
    final_listings = list(existing.values())
    
    output = {
        'version': '1.0.0',
        'updated_at': now,
        'listings': final_listings
    }
    
    with open(listings_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    active_count = sum(1 for l in final_listings if l.get('status') == 'active')
    deleted_count = sum(1 for l in final_listings if l.get('status') == 'deleted')
    print(f"Merged {len(final_listings)} listings ({active_count} active, {deleted_count} deleted)")

if __name__ == '__main__':
    merge_listings()
