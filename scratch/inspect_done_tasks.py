import json
from pathlib import Path

with open('scratch/bonsai_tasks.json', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

done_tasks = [t for t in tasks if t.get('task_status', {}).get('status') == 'Done']
print(f"Total Done tasks: {len(done_tasks)}")

parents = [t for t in tasks if not t.get('parent_task_uuid')]
for p in parents:
    subs = [t for t in tasks if t.get('parent_task_uuid') == p.get('uuid')]
    done_subs = [t for t in subs if t.get('task_status', {}).get('status') == 'Done']
    if len(done_subs) > 0 or p.get('task_status', {}).get('status') == 'Done':
        title = p.get('title')
        p_status = p.get('task_status', {}).get('status')
        print(f"\n[{p_status}] {title} ({len(done_subs)}/{len(subs)} subtasks done)")
        for s in done_subs:
            print(f"    - [{s.get('number')}] {s.get('title')}")

# Check any orphan done tasks (no parent)
orphans = [t for t in done_tasks if t.get('parent_task_uuid') and not any(p.get('uuid') == t.get('parent_task_uuid') for p in parents)]
if orphans:
    print(f"\nOrphans done: {len(orphans)}")
    for o in orphans:
        print(f"    - [{o.get('number')}] {o.get('title')}")
