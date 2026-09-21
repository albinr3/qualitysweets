import json
import re

with open('scratch/bonsai_tasks.json', 'r', encoding='utf-8') as f:
    bonsai_tasks = json.load(f)

with open('IMPLEMENTATION-ROADMAP.md', 'r', encoding='utf-8') as f:
    roadmap_text = f.read()

# Roadmap steps extraction
steps = []
current_phase = ""
for line in roadmap_text.split('\n'):
    l = line.strip()
    if l.startswith('### FASE'):
        current_phase = l
    elif l.startswith('#### Paso'):
        steps.append({
            'phase': current_phase,
            'title': l
        })

print(f"Total steps in Roadmap: {len(steps)}")
for s in steps:
    print(f"{s['phase'][:20]} | {s['title']}")

print("\n=== Bonsai Phase/Step Tasks ===")
b_phase_tasks = [t for t in bonsai_tasks if 'phase' in t.get('title', '').lower() or 'paso' in t.get('title', '').lower() or re.match(r'^\d+\.\d+[A-Z]?:', t.get('title', ''))]
print(f"Total structured tasks in Bonsai: {len(b_phase_tasks)}")
for t in sorted(b_phase_tasks, key=lambda x: x.get('number', '')):
    st = t.get('task_status', {}).get('status')
    print(f"[{t.get('number')}] ({st:<11}) {t.get('title')}")
