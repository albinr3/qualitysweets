const fs = require('fs');
const tasks = JSON.parse(fs.readFileSync('scratch/bonsai_tasks.json', 'utf8'));
const qsTasks = tasks.filter(t => t.project_id === 1535714);

console.log('=== Quality Sweets Specific Tasks ===');
const specific = qsTasks.filter(t => {
  return (t.number && t.number >= 'TSK-01100') || t.title.toLowerCase().includes('gbp') || t.title.toLowerCase().includes('roadmap') || t.title.toLowerCase().includes('phase');
});

specific.sort((a,b) => a.number.localeCompare(b.number));
specific.forEach(t => {
  const p = t.parent_task_uuid ? qsTasks.find(x => x.uuid === t.parent_task_uuid) : null;
  const parentStr = p ? `[Parent: ${p.number} - "${p.title}"]` : '[TOP LEVEL]';
  console.log(`${t.number} | ${t.task_status?.status?.padEnd(11) || 'Unknown    '} | ${parentStr.padEnd(50)} | ${t.title}`);
});
