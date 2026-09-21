import re

with open('IMPLEMENTATION-ROADMAP.md', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
current_phase = None
current_step = None

roadmap_items = []

for idx, line in enumerate(lines):
    line_str = line.strip()
    if line_str.startswith('### FASE'):
        current_phase = line_str
    elif line_str.startswith('#### Paso'):
        current_step = line_str
        # Check status in following lines
        status = "Pendiente"
        for next_line in lines[idx:min(idx+10, len(lines))]:
            if 'COMPLETADO' in next_line.upper() or 'EJECUTADO' in next_line.upper() or 'IMPLEMENTADO' in next_line.upper():
                status = "Completado"
                break
        roadmap_items.append({
            'type': 'step',
            'phase': current_phase,
            'title': current_step,
            'line': idx + 1,
            'status': status
        })
    elif re.match(r'^\*\s+\*\*Sub-paso\s+|^-\s+\*\*Sub-paso\s+|^\*\s+\*\*Paso\s+|^-\s+\*\*Paso\s+', line_str):
        status = "Pendiente"
        if 'COMPLETADO' in line_str.upper() or 'EJECUTADO' in line_str.upper() or 'IMPLEMENTADO' in line_str.upper():
            status = "Completado"
        roadmap_items.append({
            'type': 'sub-step',
            'phase': current_phase,
            'parent_step': current_step,
            'title': line_str,
            'line': idx + 1,
            'status': status
        })

print(f"Total steps found: {len(roadmap_items)}")
for item in roadmap_items:
    prefix = "  " if item['type'] == 'sub-step' else ""
    print(f"{prefix}[{item['status']}] {item['title'][:80]}")
