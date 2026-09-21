import urllib.request
import re

url = "https://cdn10.bigcommerce.com/r-7f3397d2ae83e8b48dd889540b7b618246f07f43/themes/Coffee/Styles/styles.css"
css = urllib.request.urlopen(url).read().decode('utf-8', errors='ignore')
matches = re.findall(r'([^{}]*FooterUpper[^{]*\{[^}]*\})', css, re.I)
for m in matches:
    print(m.strip())
