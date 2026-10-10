import urllib.request
import re

req = urllib.request.Request('https://qualitysweetsnj.com/menu/samosas/', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        print(f"Status: {response.status}")
        print(f"Length: {len(html)}")
        
        # Check em dashes in the main content
        em_count = html.count('—') + html.count('&mdash;')
        print(f"Em-dashes in live HTML: {em_count}")
        
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
        keywords = ['samosas', 'samosa chaat', 'Oak Tree Road', 'Iselin', 'Edison', 'Woodbridge', 'takeout', 'pickup', '$1.75', '$8.00', '$62.50', '$120.00']
        for kw in keywords:
            present = kw.lower() in html.lower()
            print(f"Keyword '{kw}': {'OK' if present else 'MISSING'}")

        # Check Schema
        has_schema = 'application/ld+json' in html and 'InStoreOnly' in html
        print(f"Schema present & InStoreOnly: {has_schema}")

        # Check avoid-ai fixes in live content
        print("Avoid AI phrase checks:")
        print("  'Why do customers travel' (should be False):", 'why do customers travel' in html.lower())
        print("  'Every day, customers drive in' (should be True):", 'every day, customers drive in' in html.lower())
        print("  'counter flow is optimized' (should be False):", 'counter flow is optimized' in html.lower())
        print("  'Everything you need to know' (should be False):", 'everything you need to know' in html.lower())
        print("  'Common questions about ordering' (should be True):", 'common questions about ordering' in html.lower())

except Exception as e:
    print(f"Error: {e}")
