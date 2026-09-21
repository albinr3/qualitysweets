const fs = require('fs');
const tasks = JSON.parse(fs.readFileSync('scratch/bonsai_tasks.json', 'utf8'));
const qsTasks = tasks.filter(t => t.project_id === 1535714);

console.log('--- ALL PARENT TASKS ---');
const parents = qsTasks.filter(t => !t.parent_task_uuid);
parents.forEach(p => {
  const subs = qsTasks.filter(t => t.parent_task_uuid === p.uuid);
  console.log(`[${p.number}] "${p.title}" | Status: ${p.task_status?.status} | Subtasks: ${subs.length}`);
});
