from pathlib import Path
from PIL import Image

root = Path(r'C:\Users\Albin Rodriguez\Downloads')
matches = []
for item in root.iterdir():
    if item.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp'}:
        continue
    try:
        with Image.open(item) as image:
            width, height = image.size
        if 900 <= width <= 1100 and 600 <= height <= 800:
            matches.append((item.name, width, height))
    except Exception:
        pass

print(f'count={len(matches)}')
for name, width, height in matches:
    print(f'{width}x{height} {name}')
