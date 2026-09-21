import json

with open('scratch/bonsai_tasks.json', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

print(f"Total tasks in local bonsai_tasks.json: {len(tasks)}")
for t in tasks:
    title = t.get('title', '').lower()
    if 'menu' in title or '4.3' in title or 'producto' in title or 'servicio' in title or 'gbp' in title:
        print(f"{t.get('number')} | ID: {t.get('uuid')} | Status: {t.get('status')} | Title: {t.get('title')}")
