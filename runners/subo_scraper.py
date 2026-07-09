#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

def scrape():
    url = 'https://www.subo.se/lediga-lagenheter/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    page_text = soup.get_text(separator='\n', strip=True)
    lines = [l.strip() for l in page_text.split('\n') if l.strip()]
    
    properties = []
    current = {}
    
    for line in lines:
        if line == 'Ledig':
            if current:
                properties.append(current)
                current = {}
        elif line.startswith('Ledigt från'):
            avail = line.replace('Ledigt från', '').replace(' eller enligt ök.', '').strip()
            current['available_from'] = avail
        elif re.match(r'^(\d+,?\d*):[aA]\s*(.+)$', line):
            m = re.match(r'^(\d+,?\d*):[aA]\s*(.+)$', line)
            current['rooms'] = m.group(1).replace(',', '.')
            rest = m.group(2).strip()
            m2 = re.match(r'^(.+?)\s+(\d{4,5}[a-zA-Z]?)\s*[,\s]*(.+)$', rest)
            if m2:
                current['street'] = m2.group(1)
                current['postal_code'] = m2.group(2)
                area = m2.group(3).strip().strip('., ')
                current['area'] = area
            else:
                parts = rest.split(',', 1)
                current['street'] = parts[0].strip()
                if len(parts) > 1:
                    current['area'] = parts[1].strip()
                else:
                    current['area'] = rest.strip()
        elif ':-/månad' in line:
            current['rent_sek'] = line.replace(':-/månad', '').strip()
        elif ' rum' in line and 'kvm' not in line:
            current['rooms_official'] = line.replace(' rum', '').strip()
        elif 'kvm' in line:
            current['size_sqm'] = line.replace('kvm', '').strip()
        elif 'kontakta Philip' in line:
            current['contact'] = 'Philip, 060-150100 tonval 4'
    
    if current:
        properties.append(current)
    
    normalized = []
    for p in properties:
        if 'street' not in p:
            continue
        address = p.get('street', '')
        postal = p.get('postal_code', '')
        area = p.get('area', '')
        normalized.append({
            'name': address,
            'address': f"{address} {postal}, {area}" if postal else f"{address}, {area}" if area else address,
            'postal_code': postal,
            'area': area,
            'rooms': p.get('rooms_official', p.get('rooms', '')),
            'size_sqm': p.get('size_sqm', ''),
            'rent_sek': p.get('rent_sek', ''),
            'available_from': p.get('available_from', ''),
            'contact': p.get('contact', ''),
            'source': 'subo',
            'url': url
        })
    
    with open('data/subo_listings.json', 'w', encoding='utf-8') as f:
        json.dump({
            'source': url,
            'extracted_at': datetime.utcnow().isoformat(),
            'properties': normalized
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(normalized)} listings")

if __name__ == '__main__':
    scrape()
