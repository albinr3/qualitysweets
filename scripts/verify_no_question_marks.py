import urllib.request

req = urllib.request.Request('https://qualitysweetsnj.com/preview-home-staging/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

lines = html.splitlines()
found_bad = []
for line in lines:
    if '?' in line:
        # Ignore query parameters in image URLs like ?c=2 or ?family=
        clean = line
        while 'http' in clean and '?c=' in clean:
            start = clean.find('http')
            end = clean.find('\"', start)
            if end == -1:
                end = clean.find("'", start)
            if end == -1:
                break
            clean = clean[:start] + clean[end+1:]
        if 'fonts.googleapis.com' in clean:
            continue
        if '?' in clean:
            found_bad.append(clean.strip())

if found_bad:
    print("Found question marks in lines:")
    for l in found_bad:
        print(" ->", l)
else:
    print("SUCCESS: 0 corrupt question marks found on the live staging page!")
