const fs = require('fs');
const tasks = JSON.parse(fs.readFileSync('scratch/bonsai_tasks.json', 'utf8'));
const qsTasks = tasks.filter(t => t.project_id === 1535714);
console.log('Total tasks in Quality Sweets project 1535714:', qsTasks.length);

// Look at all parent tasks and their subtasks
const parents = qsTasks.filter(t => !t.parent_task_uuid);
console.log('Parent tasks count:', parents.length);

parents.forEach(p => {
  const subs = qsTasks.filter(t => t.parent_task_uuid === p.uuid);
  console.log(`[${p.number}] "${p.title}" | Status: ${p.task_status?.status} (uuid: ${p.uuid}) | Subtasks: ${subs.length}`);
  subs.forEach(s => {
    console.log(`   ├── [${s.number}] "${s.title}" | Status: ${s.task_status?.status} (uuid: ${s.uuid})`);
  });
});

const subtasks = qsTasks.filter(t => t.parent_task_uuid);
console.log('Subtasks count:', subtasks.length);
const orphans = subtasks.filter(t => !parents.find(p => p.uuid === t.parent_task_uuid));
if (orphans.length > 0) {
  console.log('Orphan tasks count:', orphans.length);
  orphans.forEach(o => {
    console.log(`   ├── [${o.number}] "${o.title}" | Status: ${o.task_status?.status} | parent_uuid: ${o.parent_task_uuid}`);
  });
}
