import os
import re
import json
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")

DEST_DIR = r"C:\Users\Albin Rodriguez\Downloads\Productos_QualitySweets"
os.makedirs(DEST_DIR, exist_ok=True)

def sanitize_filename(name: str) -> str:
    # Replace characters not allowed in Windows filenames: < > : " / \ | ? *
    clean = re.sub(r'[<>:"/\\|?*]', '-', name)
    # Collapse multiple spaces or hyphens
    clean = re.sub(r'\s+', ' ', clean).strip(' .')
    return clean

def get_extension(url: str, default: str = ".jpg") -> str:
    path = urllib.parse.urlparse(url).path
    ext = os.path.splitext(path)[1].lower()
    if ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        return ext
    return default

def fetch_products():
    url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products?limit=250&include=images"
    req = urllib.request.Request(url, headers={
        "X-Auth-Token": token,
        "Accept": "application/json"
    })
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode())["data"]
    # Filter out internal store assets (ID 176)
    products = [p for p in data if p["id"] != 176]
    return products

def download_image(task):
    img_url, file_path, prod_name = task
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    req = urllib.request.Request(img_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
            with open(file_path, "wb") as f:
                f.write(content)
        size_kb = len(content) / 1024
        return (True, prod_name, os.path.basename(file_path), size_kb, None)
    except Exception as e:
        return (False, prod_name, os.path.basename(file_path), 0, str(e))

def main():
    print(f"Obteniendo catálogo de productos de BigCommerce...")
    products = fetch_products()
    print(f"Total productos reales a procesar: {len(products)}")

    download_tasks = []
    
    for prod in sorted(products, key=lambda x: x["id"]):
        images = prod.get("images", [])
        if not images:
            print(f"[-] Producto sin imagen: ID {prod['id']} - {prod['name']}")
            continue
        
        clean_name = sanitize_filename(prod["name"])
        total_imgs = len(images)
        
        for idx, img in enumerate(images, start=1):
            img_url = img.get("url_zoom") or img.get("url_standard")
            if not img_url:
                continue
            ext = get_extension(img_url)
            
            if total_imgs == 1:
                filename = f"{clean_name}{ext}"
            else:
                filename = f"{clean_name} - {idx}{ext}"
            
            file_path = os.path.join(DEST_DIR, filename)
            download_tasks.append((img_url, file_path, prod["name"]))

    print(f"\nIniciando descarga de {len(download_tasks)} imágenes en '{DEST_DIR}' con 8 hilos...")

    successful = 0
    failed = 0
    results = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(download_image, t) for t in download_tasks]
        for f in as_completed(futures):
            ok, prod_name, filename, size_kb, err = f.result()
            if ok:
                successful += 1
                results.append((prod_name, filename, size_kb))
                print(f"[OK] ({successful}/{len(download_tasks)}) {filename} ({size_kb:.1f} KB)")
            else:
                failed += 1
                print(f"[ERROR] Falló {filename} para {prod_name}: {err}")

    print("\n" + "="*60)
    print(f"RESUMEN DE DESCARGA:")
    print(f"Destino: {DEST_DIR}")
    print(f"Total descargadas con éxito: {successful}")
    print(f"Total fallidas: {failed}")
    print("="*60)

if __name__ == "__main__":
    main()
