import urllib.request
import re

req = urllib.request.Request('https://qualitysweetsnj.com/menu/pani-puri/', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        print(f"Status: {response.status}")
        print(f"Length: {len(html)}")
        
        # Check titles / headings
        h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
        print(f"H1 count in HTML markup: {len(h1s)}")
        for i, h in enumerate(h1s):
            clean_h = re.sub(r'<[^>]+>', '', h).strip()
            print(f"  H1 #{i+1}: {clean_h}")
            
        h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL | re.IGNORECASE)
        print(f"H2 count: {len(h2s)}")
        for i, h in enumerate(h2s):
            clean_h = re.sub(r'<[^>]+>', '', h).strip()
            print(f"  H2 #{i+1}: {clean_h}")

        # Check keywords
        keywords = ['pani puri', 'gol gappe', 'puchka', 'Oak Tree Road', 'Iselin', 'Edison', 'Woodbridge', '$8.00', '$28.00', '$45.00', '$85.00', 'takeout', 'pickup']
        for kw in keywords:
            present = kw.lower() in html.lower()
            print(f"Keyword '{kw}': {'OK' if present else 'MISSING'}")

        # Check Schema
        has_schema = 'application/ld+json' in html and 'InStoreOnly' in html and 'pani-puri' in html
        print(f"Schema present, InStoreOnly & pani-puri: {has_schema}")

except Exception as e:
    print(f"Error: {e}")
