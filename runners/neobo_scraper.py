#!/usr/bin/env python3

import requests
import json
import re
from datetime import datetime

def extract_next_data(html):
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return None

def scrape():
    api_url = 'https://www.neobo.se/sv/wp-json/properties/homeq/'
    params = {
        'p': 1
    }
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }
    
    response = requests.get(api_url, params=params, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    properties = []
    
    for prop in data.get('properties', []):
        listing_url = prop.get('url', '')
        available_from = ''
        
        if listing_url and 'homeq.se/lagenhet/' in listing_url:
            try:
                detail_resp = requests.get(listing_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
                detail_resp.raise_for_status()
                next_data = extract_next_data(detail_resp.text)
                if next_data:
                    object_ad = next_data.get('props', {}).get('pageProps', {}).get('objectAd', {})
                    date_access = object_ad.get('date_access')
                    if date_access:
                        available_from = date_access
            except Exception as e:
                print(f"Warning: failed to fetch detail page {listing_url}: {e}")
        
        properties.append({
            'id': prop.get('external_id', ''),
            'name': prop.get('name', ''),
            'address': prop.get('name', ''),
            'area': prop.get('city', 'Sundsvall'),
            'rooms': prop.get('rooms', ''),
            'size_sqm': prop.get('size', ''),
            'rent_sek': prop.get('rent', ''),
            'available_from': available_from,
            'url': listing_url,
            'source': 'neobo'
        })
    
    with open('data/neobo_listings.json', 'w', encoding='utf-8') as f:
        json.dump({
            'source': api_url,
            'extracted_at': datetime.utcnow().isoformat(),
            'properties': properties
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(properties)} listings")

if __name__ == '__main__':
    scrape()
