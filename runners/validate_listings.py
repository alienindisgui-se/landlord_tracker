#!/usr/bin/env python3
"""Validate data/listings.json against schemas/listing.schema.json"""
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema is not installed. Run: pip install jsonschema")
    sys.exit(1)

REPO = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO / "schemas" / "listing.schema.json"
LISTINGS_PATH = REPO / "data" / "listings.json"

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema = json.load(f)

if not LISTINGS_PATH.exists():
    print(f"ERROR: {LISTINGS_PATH} does not exist")
    sys.exit(1)

with open(LISTINGS_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

listings = data.get("listings", [])
errors = []

for idx, listing in enumerate(listings):
    try:
        jsonschema.validate(instance=listing, schema=schema)
    except jsonschema.ValidationError as e:
        errors.append({
            "index": idx,
            "source": listing.get("source"),
            "id": listing.get("id"),
            "name": listing.get("name"),
            "error": str(e)
        })

print(f"Validated {len(listings)} listings against {SCHEMA_PATH}")

if errors:
    print(f"FAILED: {len(errors)} invalid listing(s)")
    for err in errors:
        print(f"  [{err['index']}] {err['source']} | {err['name']} | {err['id']} | {err['error']}")
    sys.exit(1)
else:
    print("OK: all listings are valid")
    sys.exit(0)
