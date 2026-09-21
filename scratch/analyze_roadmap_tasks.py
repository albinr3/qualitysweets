import json

with open('scratch/bonsai_tasks.json', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

phase_tasks = [t for t in tasks if 'phase' in t.get('title', '').lower() or 'paso' in t.get('title', '').lower() or any(f'{p}.' in t.get('title', '') for p in [1, 2, 3, 4, 5])]

print(f"Total tasks in local backup: {len(tasks)}")
print(f"Roadmap matching tasks: {len(phase_tasks)}")
for t in sorted(phase_tasks, key=lambda x: x.get('title', '')):
    print(f"{t.get('number')} | Status: {t.get('status')} | {t.get('title')}")
