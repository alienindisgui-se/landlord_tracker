#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def scrape():
    url = 'https://www.neobo.se/sv/wp-json/properties/homeq/'
    params = {
        'p': 1,
        'municipality': 'Sundsvall'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    properties = []
    
    for prop in data.get('properties', []):
        properties.append({
            'id': prop.get('external_id', ''),
            'name': prop.get('name', ''),
            'address': prop.get('name', ''),
            'area': prop.get('city', 'Sundsvall'),
            'rooms': prop.get('rooms', ''),
            'size_sqm': prop.get('size', ''),
            'rent_sek': prop.get('rent', ''),
            'url': prop.get('url', ''),
            'source': 'neobo'
        })
    
    with open('data/neobo_listings.json', 'w', encoding='utf-8') as f:
        json.dump({
            'source': url,
            'extracted_at': datetime.utcnow().isoformat(),
            'properties': properties
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(properties)} listings")

if __name__ == '__main__':
    scrape()
