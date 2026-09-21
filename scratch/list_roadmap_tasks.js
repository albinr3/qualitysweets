const fs = require('fs');
const tasks = JSON.parse(fs.readFileSync('scratch/bonsai_tasks.json', 'utf8'));
const qsTasks = tasks.filter(t => t.project_id === 1535714);

const roadmapParents = qsTasks.filter(t => {
  return t.title.startsWith('Phase ') || t.title.includes('gbp') || t.title.includes('menu') || t.title.includes('Step ');
});

roadmapParents.sort((a, b) => a.number.localeCompare(b.number));

roadmapParents.forEach(p => {
  const subs = qsTasks.filter(t => t.parent_task_uuid === p.uuid);
  console.log(`\n=== [${p.number}] "${p.title}" | Status: ${p.task_status?.status} (uuid: ${p.uuid}) ===`);
  subs.forEach(s => {
    console.log(`   ├── [${s.number}] "${s.title}" | Status: ${s.task_status?.status} (uuid: ${s.uuid})`);
  });
});
