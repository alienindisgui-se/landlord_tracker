#!/usr/bin/env python3

import json
from datetime import datetime
from pathlib import Path

def merge_listings():
    data_dir = Path('data')
    
    sources = ['subo', 'sveafastigheter', 'neobo']
    all_listings = []
    
    for source in sources:
        src_file = data_dir / f'{source}_listings.json'
        if src_file.exists():
            with open(src_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_listings.extend(data.get('properties', []))
    
    output = {
        'updated_at': datetime.utcnow().isoformat(),
        'listings': all_listings
    }
    
    with open(data_dir / 'listings.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Merged {len(all_listings)} listings")

if __name__ == '__main__':
    merge_listings()
