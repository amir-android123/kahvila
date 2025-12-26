import re
import json
from urllib.parse import unquote

# Read the HTML file
with open(r'c:\Bon Bon\wolt-source.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all URL-encoded JSON data containing product information
# Look for patterns like %22items%22%3A%5B which is "items":[

# First, let's find and decode the main data blob
# The data appears to be in a script tag with encoded JSON

# Find all imageproxy URLs with product names
pattern = r'%22name%22%3A%22([^%]+(?:%[0-9A-F]{2}[^%]*)*)%22.*?%22images%22%3A%5B%7B%22url%22%3A%22(https%3A%2F%2Fimageproxy\.wolt\.com%2Fassets%2F[a-f0-9]+)%22'

matches = re.findall(pattern, content, re.IGNORECASE)

products = []
seen_names = set()

for name_encoded, url_encoded in matches:
    name = unquote(name_encoded)
    url = unquote(url_encoded)
    
    # Skip category names and duplicates
    if name not in seen_names:
        seen_names.add(name)
        products.append({
            'name': name,
            'image_url': url
        })

# Also search for the reverse pattern (images before name)
pattern2 = r'%22images%22%3A%5B%7B%22url%22%3A%22(https%3A%2F%2Fimageproxy\.wolt\.com%2Fassets%2F[a-f0-9]+)%22.*?%22name%22%3A%22([^%]+(?:%[0-9A-F]{2}[^%]*)*)%22'

matches2 = re.findall(pattern2, content, re.IGNORECASE)

for url_encoded, name_encoded in matches2:
    name = unquote(name_encoded)
    url = unquote(url_encoded)
    
    if name not in seen_names:
        seen_names.add(name)
        products.append({
            'name': name,
            'image_url': url
        })

print(f"Found {len(products)} products:\n")
for p in products:
    print(f"Product: {p['name']}")
    print(f"Image URL: {p['image_url']}")
    print("-" * 80)
