import os
import shutil
from pathlib import Path

src_dir = Path(r"C:\Users\Albin Rodríguez\.gemini\antigravity-ide\brain\e17892fb-2fbd-493d-914e-eb9f45a30db3\.user_uploaded")
dest_dir = Path("content/catering/images")
dest_dir.mkdir(parents=True, exist_ok=True)

dest_assets = Path("assets/catering")
dest_assets.mkdir(parents=True, exist_ok=True)

mapping = {
    "media_1790699837581.jpg": "bulk-jalebi-catering-trays-iselin-nj.jpg",
    "media_1790699837658.jpg": "bulk-samosa-catering-party-trays-nj.jpg",
    "media_1790699837699.jpg": "bulk-namkeen-savory-snack-order.jpg",
    "media_1790700310373.jpg": "handcrafted-mithai-kitchen-preparation.jpg"
}

for src_name, dest_name in mapping.items():
    src_file = src_dir / src_name
    shutil.copy2(src_file, dest_dir / dest_name)
    shutil.copy2(src_file, dest_assets / dest_name)
    print(f"Copied {src_name} -> {dest_name}")
