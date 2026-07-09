#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape():
    url = 'https://sveafastigheter.se/se-alla-lediga-lagenheter-for-uthyrning?kommun=Sundsvall'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    properties = []
    
    # Extract only Sundsvall listings
    items = soup.select('li.homeq_item.filter_Sundsvall.displayed')
    
    for item in items:
        data_id = item.get('data-id', '')
        title = item.get('data-title', '')
        city = item.get('data-city', 'Sundsvall')
        inflytt = item.get('data-inflytt', '')
        hyra = item.get('data-hyra', '')
        rum = item.get('data-rum', '')
        publish = item.get('data-publish', '')
        href = item.select_one('a')['href'] if item.select_one('a') else ''
        
        # Extract additional details from HTML
        info_container = item.select_one('div.homeq_info_container')
        rooms_text = ''
        size_text = ''
        rent_text = ''
        inflytt_text = ''
        
        if info_container:
            # Get text from info_bottom div
            info_bottom = info_container.select_one('div.homeq_info_bottom')
            if info_bottom:
                inflytt_text = info_bottom.find('span').text.strip() if info_bottom.find('span') else ''
                
                lower_div = info_bottom.select_one('div.lower')
                if lower_div:
                    spans = lower_div.find_all('span')
                    for span in spans:
                        text = span.text.strip()
                        if 'ROK' in text:
                            rooms_text = text
                        elif 'm²' in text:
                            size_text = text
                        elif 'kr' in text:
                            rent_text = text
        
        properties.append({
            'id': data_id,
            'name': title,
            'address': title,
            'area': city,
            'rooms': rooms_text or rum,
            'rooms_raw': rum,
            'size_sqm': size_text,
            'rent_sek': rent_text or hyra,
            'rent_raw': hyra,
            'available_from': inflytt_text or inflytt,
            'available_raw': inflytt,
            'published_at': publish,
            'url': f"https://sveafastigheter.se{href}" if href.startswith('/') else href,
            'source': 'sveafastigheter'
        })
    
    # Save structured JSON
    with open('data/sveafastigheter_listings.json', 'w', encoding='utf-8') as f:
        json.dump({
            'source': url,
            'extracted_at': datetime.utcnow().isoformat(),
            'properties': properties
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(properties)} Sundsvall listings")

if __name__ == '__main__':
    scrape()
