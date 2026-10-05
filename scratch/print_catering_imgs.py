import re

with open("scratch/category_21_desc.html", "r", encoding="utf-8") as f:
    html = f.read()

imgs = re.findall(r'<img[^>]*>', html)
for i, img in enumerate(imgs, 1):
    print(f"[{i}] {img}\n")
