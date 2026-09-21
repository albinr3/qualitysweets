const fs = require('fs');
const tasks = JSON.parse(fs.readFileSync('scratch/bonsai_tasks.json', 'utf8'));
const qsTasks = tasks.filter(t => t.project_id === 1535714);

const earlyTasks = qsTasks.filter(t => {
  return t.number && t.number >= 'TSK-01100' && t.number <= 'TSK-01140';
});
earlyTasks.sort((a, b) => a.number.localeCompare(b.number));

earlyTasks.forEach(t => {
  console.log(`[${t.number}] "${t.title}" | Status: ${t.task_status?.status} (uuid: ${t.uuid}, parent: ${t.parent_task_uuid})`);
});
