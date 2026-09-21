import urllib.request

req = urllib.request.Request('https://qualitysweetsnj.com/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

start = html.find("$('.slide-show').flexslider")
if start != -1:
    script_start = html.rfind('<script', 0, start)
    script_end = html.find('</script>', start) + 9
    print("FLEXSLIDER SCRIPT:")
    print(html[script_start:script_end])
