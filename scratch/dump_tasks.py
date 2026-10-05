import json

with open('scratch/bonsai_tasks.json', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

parents = [t for t in tasks if not t.get('parent_task_uuid')]

with open('scratch/all_done_tasks_summary.txt', 'w', encoding='utf-8') as out:
    out.write(f"TOTAL TASKS: {len(tasks)}\n")
    done_count = sum(1 for t in tasks if t.get('task_status', {}).get('status') == 'Done')
    out.write(f"DONE TASKS: {done_count}\n\n")
    
    for p in parents:
        subs = [t for t in tasks if t.get('parent_task_uuid') == p.get('uuid')]
        done_subs = [t for t in subs if t.get('task_status', {}).get('status') == 'Done']
        title = p.get('title')
        p_status = p.get('task_status', {}).get('status')
        out.write(f"=== [{p_status}] {title} ({len(done_subs)}/{len(subs)} subtasks done) ===\n")
        for s in done_subs:
            out.write(f"  * [{s.get('number')}] {s.get('title')}\n")
        out.write("\n")

print("Done writing scratch/all_done_tasks_summary.txt")
