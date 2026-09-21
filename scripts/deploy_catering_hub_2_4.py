"""Deploy the single-source Catering & Bulk Orders landing to BigCommerce.

The local content/catering/index.html file is the source of truth.  This script:
1. updates category 21 (/catering/) and its SEO metadata;
2. removes the obsolete specialty web pages that duplicate the landing; and
3. creates permanent redirects to the relevant section of /catering/.

Run with --dry-run to inspect the intended changes without calling BigCommerce.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DOMAIN = "https://qualitysweetsnj.com"
CATEGORY_ID = 21
SEO_TITLE = "Indian Catering & Bulk Orders in NJ, NY & CT | Quality Sweets"
SEO_DESCRIPTION = (
    "Indian catering and bulk orders for NJ, NY & CT. Fresh samosas, mithai, "
    "wedding sweets, temple orders and event snacks from Quality Sweets."
)
OBSOLETE_PAGES = {
    "/catering/wedding-catering-tri-state/": "/catering/#weddings",
    "/catering/temple-mandir-bulk-prasad/": "/catering/#temple-orders",
    "/catering/bulk-samosa-orders/": "/catering/#bulk-orders",
}


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip().strip('"').strip("'")
    return values


ENV = load_env()
STORE_HASH = ENV.get("BIGCOMMERCE_STORE_HASH") or os.getenv("BIGCOMMERCE_STORE_HASH")
ACCESS_TOKEN = ENV.get("BIGCOMMERCE_ACCESS_TOKEN") or os.getenv("BIGCOMMERCE_ACCESS_TOKEN")
CLIENT_ID = ENV.get("BIGCOMMERCE_CLIENT_ID") or os.getenv("BIGCOMMERCE_CLIENT_ID")
API_ROOT = f"https://api.bigcommerce.com/stores/{STORE_HASH}" if STORE_HASH else ""


def headers() -> dict[str, str]:
    result = {
        "X-Auth-Token": ACCESS_TOKEN or "",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if CLIENT_ID:
        result["X-Auth-Client"] = CLIENT_ID
    return result


def request_json(path: str, method: str = "GET", payload: object | None = None) -> tuple[int, object]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        f"{API_ROOT}{path}", data=data, headers=headers(), method=method
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} failed with HTTP {error.code}: {body}") from error


def validate_config() -> None:
    missing = [
        name for name, value in {
            "BIGCOMMERCE_STORE_HASH": STORE_HASH,
            "BIGCOMMERCE_ACCESS_TOKEN": ACCESS_TOKEN,
        }.items() if not value
    ]
    if missing:
        raise RuntimeError("Missing required .env values: " + ", ".join(missing))


def validate_local_content() -> str:
    content_path = BASE_DIR / "content" / "catering" / "index.html"
    body = content_path.read_text(encoding="utf-8")
    required = [
        "Indian Catering &amp; Bulk Orders in NJ, NY &amp; CT",
        'id="weddings"',
        'id="bulk-orders"',
        'id="temple-orders"',
        "Samosa Catering &amp; Bulk Orders",
        "Request a Catering Quote",
    ]
    absent = [item for item in required if item not in body]
    if absent:
        raise RuntimeError("Local catering file is missing expected content: " + ", ".join(absent))
    return body


def update_category(body: str, dry_run: bool) -> None:
    payload = {
        "name": "Indian Catering & Bulk Orders in NJ, NY & CT",
        "description": body,
        "is_visible": True,
        "page_title": SEO_TITLE,
        "meta_description": SEO_DESCRIPTION,
    }
    if dry_run:
        print(f"[DRY RUN] PUT /v2/categories/{CATEGORY_ID}")
        return
    status, response = request_json(f"/v2/categories/{CATEGORY_ID}", "PUT", payload)
    if status != 200:
        raise RuntimeError(f"Unexpected category response: HTTP {status}")
    print(f"[OK {status}] Updated category {CATEGORY_ID}: {response.get('url', '/catering/')}")


def remove_obsolete_pages(dry_run: bool) -> None:
    if dry_run:
        for source in OBSOLETE_PAGES:
            print(f"[DRY RUN] Locate then DELETE obsolete web page {source}")
        return
    _, pages = request_json("/v2/pages")
    pages_by_path = {
        page.get("url", "").rstrip("/"): page
        for page in pages
        if isinstance(page, dict) and page.get("url")
    }
    for source in OBSOLETE_PAGES:
        page = pages_by_path.get(source.rstrip("/"))
        if not page:
            print(f"[SKIP] Obsolete page already absent: {source}")
            continue
        status, _ = request_json(f"/v2/pages/{page['id']}", "DELETE")
        if status not in (200, 204):
            raise RuntimeError(f"Unexpected delete response for page {page['id']}: HTTP {status}")
        print(f"[OK {status}] Deleted obsolete page {page['id']}: {source}")


def create_redirects(dry_run: bool) -> None:
    if dry_run:
        for source, destination in OBSOLETE_PAGES.items():
            print(f"[DRY RUN] POST /v2/redirects {source} -> {destination}")
        return
    _, existing_redirects = request_json("/v2/redirects")
    by_path = {
        redirect.get("path", "").rstrip("/"): redirect
        for redirect in existing_redirects
        if isinstance(redirect, dict) and redirect.get("path")
    }
    for source, destination in OBSOLETE_PAGES.items():
        # Legacy Blueprint stores category redirects by reference, which is more
        # reliable than a manual URL (and keeps every historical URL canonical).
        payload = {"path": source, "forward": {"type": "category", "ref": str(CATEGORY_ID)}}
        existing = by_path.get(source.rstrip("/"))
        if existing:
            forward = existing.get("forward", {})
            if forward.get("type") == "category" and str(forward.get("ref")) == str(CATEGORY_ID):
                print(f"[SKIP] Redirect already canonical: {source} -> /catering/")
                continue
            status, _ = request_json(f"/v2/redirects/{existing['id']}", "PUT", payload)
            action = "Updated"
        else:
            status, _ = request_json("/v2/redirects", "POST", payload)
            action = "Created"
        if status not in (200, 201):
            raise RuntimeError(f"Unexpected redirect response for {source}: HTTP {status}")
        print(f"[OK {status}] {action} permanent redirect {source} -> {destination}")


def verify_live_urls() -> bool:
    expected = {f"{DOMAIN}/catering/": 200}
    expected.update({f"{DOMAIN}{path}": 301 for path in OBSOLETE_PAGES})
    all_ok = True
    for url, expected_status in expected.items():
        request = urllib.request.Request(url, headers={"User-Agent": "QualitySweets deployment verifier"})
        try:
            opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
            # A custom no-redirect handler preserves the actual 301 for legacy paths.
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, hdrs, newurl):
                    return None
            opener = urllib.request.build_opener(NoRedirect)
            with opener.open(request, timeout=20) as response:
                status = response.status
        except urllib.error.HTTPError as error:
            status = error.code
        ok = status == expected_status
        all_ok = all_ok and ok
        print(f"[{'OK' if ok else 'ERROR'} {status}] {url} (expected {expected_status})")
    return all_ok


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Validate without REST writes")
    args = parser.parse_args()
    try:
        validate_config()
        body = validate_local_content()
        print("=== Deploying the unified /catering/ landing ===")
        update_category(body, args.dry_run)
        remove_obsolete_pages(args.dry_run)
        create_redirects(args.dry_run)
        if args.dry_run:
            print("[DRY RUN] Local validation completed; no BigCommerce data was changed.")
            return 0
        print("=== Verifying production ===")
        return 0 if verify_live_urls() else 1
    except (OSError, RuntimeError) as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
