import os
import json
import urllib.request
import urllib.error

def load_env():
    env_vars = {}
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    env_vars[key.strip()] = val.strip().strip('"').strip("'")
    return env_vars

def test_api():
    env = load_env()
    store_hash = env.get("BIGCOMMERCE_STORE_HASH") or os.environ.get("BIGCOMMERCE_STORE_HASH")
    access_token = env.get("BIGCOMMERCE_ACCESS_TOKEN") or os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")
    client_id = env.get("BIGCOMMERCE_CLIENT_ID") or os.environ.get("BIGCOMMERCE_CLIENT_ID")

    if not store_hash or not access_token:
        print("[ERROR] Faltan credenciales en el archivo .env.")
        print("Asegurate de definir BIGCOMMERCE_STORE_HASH y BIGCOMMERCE_ACCESS_TOKEN.")
        return False

    headers = {
        "X-Auth-Token": access_token,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    if client_id:
        headers["X-Auth-Client"] = client_id

    print(f"-> Conectando con la tienda BigCommerce (Store Hash: {store_hash})...\n")

    # 1. Probar información general de la tienda (/v2/store)
    try:
        url_store = f"https://api.bigcommerce.com/stores/{store_hash}/v2/store"
        req = urllib.request.Request(url_store, headers=headers, method="GET")
        with urllib.request.urlopen(req) as resp:
            store_data = json.loads(resp.read().decode("utf-8"))
            print("[OK] Conexión básica exitosa!")
            print(f"     - Nombre de la Tienda: {store_data.get('name')}")
            print(f"     - Dominio: {store_data.get('domain')}")
            print(f"     - Plan: {store_data.get('plan_name')}")
            print(f"     - Moneda: {store_data.get('currency')}")
    except urllib.error.HTTPError as e:
        print(f"[FALLO] Error al consultar /v2/store (HTTP {e.code}): {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"[FALLO] Error de conexión: {str(e)}")
        return False

    # 2. Probar acceso a Páginas (/v3/content/pages)
    try:
        url_pages = f"https://api.bigcommerce.com/stores/{store_hash}/v3/content/pages"
        req = urllib.request.Request(url_pages, headers=headers, method="GET")
        with urllib.request.urlopen(req) as resp:
            pages_data = json.loads(resp.read().decode("utf-8"))
            pages_list = pages_data.get("data", [])
            print(f"\n[OK] Permiso de Páginas (Content API) activo!")
            print(f"     - Total de páginas existentes: {len(pages_list)}")
            for p in pages_list[:5]:
                print(f"       * [{p.get('id')}] {p.get('name')} -> {p.get('url')}")
            if len(pages_list) > 5:
                print(f"       * ... y {len(pages_list) - 5} páginas más.")
    except urllib.error.HTTPError as e:
        print(f"\n[AVISO] No se pudo leer /v3/content/pages (HTTP {e.code}): Verifica el scope 'Content'")

    # 3. Probar acceso a Ajustes SEO (/v3/settings/storefront/seo)
    try:
        url_seo = f"https://api.bigcommerce.com/stores/{store_hash}/v3/settings/storefront/seo"
        req = urllib.request.Request(url_seo, headers=headers, method="GET")
        with urllib.request.urlopen(req) as resp:
            seo_data = json.loads(resp.read().decode("utf-8")).get("data", {})
            print(f"\n[OK] Permiso de Ajustes SEO (Settings API) activo!")
            print(f"     - Title Tag actual: {seo_data.get('page_title') or '(Vacio)'}")
            print(f"     - Meta Description actual: {seo_data.get('meta_description') or '(Vacio)'}")
    except urllib.error.HTTPError as e:
        print(f"\n[AVISO] No se pudo leer /v3/settings/storefront/seo (HTTP {e.code}): Verifica el scope 'Store Settings'")

    # 4. Probar acceso a Categorías (/v3/catalog/categories)
    try:
        url_cat = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories?limit=5"
        req = urllib.request.Request(url_cat, headers=headers, method="GET")
        with urllib.request.urlopen(req) as resp:
            cat_data = json.loads(resp.read().decode("utf-8")).get("data", [])
            print(f"\n[OK] Permiso de Catálogo/Categorías activo!")
            print(f"     - Muestra de categorías:")
            for c in cat_data:
                print(f"       * [ID {c.get('id')}] {c.get('name')} -> {c.get('custom_url', {}).get('url')}")
    except urllib.error.HTTPError as e:
        print(f"\n[AVISO] No se pudo leer /v3/catalog/categories (HTTP {e.code}): Verifica el scope 'Products'")

    print("\n==========================================")
    print(" Verificación completada con éxito ")
    print("==========================================")
    return True

if __name__ == "__main__":
    test_api()
