import os
from pathlib import Path
from PIL import Image

images = [
    ("bulk-jalebi-catering-trays-iselin-nj.jpg", (800, 1067)),
    ("bulk-samosa-catering-party-trays-nj.jpg", (800, 1067)),
    ("bulk-namkeen-savory-snack-order.jpg", (800, 1006)),
    ("handcrafted-mithai-kitchen-preparation.jpg", (1024, 576))
]

img_dir = Path("content/catering/images")
webp_dir = img_dir / "webp"
webp_dir.mkdir(parents=True, exist_ok=True)

for name, max_size in images:
    src_path = img_dir / name
    with Image.open(src_path) as im:
        im.thumbnail(max_size, Image.Resampling.LANCZOS)
        # Save optimized JPG
        im.save(src_path, "JPEG", quality=84, optimize=True)
        print(f"Optimized JPG {name}: {os.path.getsize(src_path)} bytes, size={im.size}")
        
        # Save WebP
        webp_name = name.replace(".jpg", ".webp")
        webp_path = webp_dir / webp_name
        im.save(webp_path, "WEBP", quality=82)
        print(f"Saved WebP {webp_name}: {os.path.getsize(webp_path)} bytes")
