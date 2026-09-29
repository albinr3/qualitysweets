import os
from PIL import Image

src_dir = r"C:\Users\Albin Rodríguez\.gemini\antigravity-ide\brain\e17892fb-2fbd-493d-914e-eb9f45a30db3\.user_uploaded"
files = [
    "media_1790699837581.jpg",
    "media_1790699837658.jpg",
    "media_1790699837699.jpg",
    "media_1790700310373.jpg"
]

for f in files:
    path = os.path.join(src_dir, f)
    with Image.open(path) as img:
        print(f"{f}: size={img.size}, format={img.format}, mode={img.mode}")
