#!/usr/bin/env python3

import json
import os
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

def enrich_neighborhood():
    data_dir = Path('data')
    listings_path = data_dir / 'listings.json'
    
    if not listings_path.exists():
        print("No listings.json found")
        return
    
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("GEMINI_API_KEY not set, skipping enrichment")
        return
    
    with open(listings_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    enriched_count = 0
    skipped_count = 0
    
    for listing in data.get('listings', []):
        if listing.get('neighborhood_summary'):
            skipped_count += 1
            continue
        
        area = listing.get('area', '')
        address = listing.get('address', '')
        
        if not area and not address:
            continue
        
        prompt = (
            f"Provide a concise neighborhood summary (max 80 words) for a rental listing "
            f"in {area or address}, Sweden. Focus on: transport links, local amenities, "
            f"and what makes the area desirable. Keep it factual and neutral."
        )
        
        try:
            summary = call_gemini_flash(api_key, prompt)
            if summary:
                listing['neighborhood_summary'] = summary
                enriched_count += 1
        except Exception as e:
            print(f"Failed to enrich listing {listing.get('id')}: {e}")
    
    with open(listings_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Enriched {enriched_count} listings, skipped {skipped_count} with existing summaries")

def call_gemini_flash(api_key, prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 200,
            "candidateCount": 1
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        f"{url}?key={api_key}",
        data=data,
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            return text.strip() if text else None
    except urllib.error.HTTPError as e:
        print(f"Gemini API error: {e.code} - {e.read().decode()}")
        return None
    except Exception as e:
        print(f"Gemini API exception: {e}")
        return None

if __name__ == '__main__':
    enrich_neighborhood()
