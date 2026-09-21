const https = require('https');
const fs = require('fs');

const BONSAI_TOKEN = 'bonsai_at_6DmXce5_xF66dEgF5_B1cHlJnk6O_-UHXhUcYi3Ztv8';
const DONE_STATUS_ID = '2b37479a-fb6d-4685-b7c7-7600a21bd141';

const completedNumbers = [
  // ACCESS
  'TSK-00394', 'TSK-00397', 'TSK-00398', 'TSK-00399', 'TSK-00400',
  // BASELINE
  'TSK-00407', 'TSK-00408', 'TSK-00409', 'TSK-00410', 'TSK-00411', 'TSK-00412', 'TSK-00413', 'TSK-00414',
  // TRACKING SETUP
  'TSK-00415', 'TSK-00417', 'TSK-00418', 'TSK-00419', 'TSK-00420', 'TSK-00421',
  // RESEARCH
  'TSK-00422', 'TSK-00425', 'TSK-00426', 'TSK-00427', 'TSK-00428',
  // KEYWORD & URL MAPPING
  'TSK-00429', 'TSK-00431', 'TSK-00432', 'TSK-00433', 'TSK-00434', 'TSK-00435', 'TSK-00436',
  // WEBSITE / TECHNICAL AUDIT
  'TSK-00437', 'TSK-00438', 'TSK-00439', 'TSK-00440', 'TSK-00441',
  // SITE ARCHITECTURE & PAGE PLAN
  'TSK-00442', 'TSK-00443', 'TSK-00444', 'TSK-00445', 'TSK-00446', 'TSK-00447', 'TSK-00448', 'TSK-00449', 'TSK-00450', 'TSK-00451',
  // PAGE STRATEGY / SEO BRIEFS
  'TSK-00452', 'TSK-00453', 'TSK-00454', 'TSK-00455', 'TSK-00456', 'TSK-00457', 'TSK-00458', 'TSK-00459', 'TSK-00460', 'TSK-00461', 'TSK-00462', 'TSK-00463', 'TSK-00464', 'TSK-00465', 'TSK-00466',
  // SEO STRATEGY + PRIORITIZATION
  'TSK-00467', 'TSK-00468', 'TSK-00469', 'TSK-00470', 'TSK-00471', 'TSK-00472',
  // WEBSITE INITIAL IMPLEMENTATION
  'TSK-00473', 'TSK-00474', 'TSK-00475', 'TSK-00476', 'TSK-00477', 'TSK-00478', 'TSK-00479', 'TSK-00480', 'TSK-00481',
  // TECHNICAL SEO SETUP
  'TSK-00482', 'TSK-00483', 'TSK-00485', 'TSK-00486', 'TSK-00487',
  // LOCAL LISTINGS + GBP INITIAL OPTIMIZATION
  'TSK-00488', 'TSK-00489', 'TSK-00494', 'TSK-00495', 'TSK-00496', 'TSK-00501',
  // QA
  'TSK-00504', 'TSK-00507', 'TSK-00508',
  // PHASE 3 SPECIFICS
  'TSK-01154', 'TSK-01157', 'TSK-01158', 'TSK-01159', 'TSK-01160',
  // PHASE 4 SPECIFICS
  'TSK-01164', 'TSK-01168', 'TSK-01169', 'TSK-01170',
  'TSK-01165', 'TSK-01171', 'TSK-01172',
  // RECENT QUALITY SWEETS SPECIFICS
  'TSK-01192', 'TSK-01193', 'TSK-01194', 'TSK-01643'
];

function request(method, path, headers, body) {
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'mcp.hellobonsai.com',
      path: path,
      method: method,
      headers: headers
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body: data }));
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function run() {
  const allTasks = JSON.parse(fs.readFileSync('scratch/bonsai_tasks.json', 'utf8'));
  
  const initPayload = JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'initialize',
    params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'sync-script', version: '1.0' } }
  });

  const res1 = await request('POST', '/mcp', {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/event-stream',
    'Authorization': `Bearer ${BONSAI_TOKEN}`
  }, initPayload);

  let sessionId = res1.headers['mcp-session-id'];
  console.log('Connected to Bonsai MCP. Session:', sessionId);

  // Filter tasks that need update
  const tasksToUpdate = allTasks.filter(t => 
    completedNumbers.includes(t.number) && 
    t.number !== 'TSK-01194' && 
    t.number !== 'TSK-01193'
  );

  console.log(`Found ${tasksToUpdate.length} tasks to update to Done.\n`);

  let successCount = 0;
  let failCount = 0;
  const updatedList = [];

  for (let i = 0; i < tasksToUpdate.length; i++) {
    const task = tasksToUpdate[i];
    const callPayload = JSON.stringify({
      jsonrpc: '2.0',
      id: i + 2,
      method: 'tools/call',
      params: {
        name: 'update_task',
        arguments: {
          uuid: task.uuid,
          task_status_id: DONE_STATUS_ID
        }
      }
    });

    let attempts = 0;
    let success = false;

    while (attempts < 3 && !success) {
      attempts++;
      try {
        const res = await request('POST', '/mcp', {
          'Content-Type': 'application/json',
          'Accept': 'application/json, text/event-stream',
          'Authorization': `Bearer ${BONSAI_TOKEN}`,
          'Mcp-Session-Id': sessionId
        }, callPayload);

        if (res.status === 200) {
          success = true;
          successCount++;
          updatedList.push({ number: task.number, title: task.title, uuid: task.uuid });
          console.log(`[${i + 1}/${tasksToUpdate.length}] ✅ Updated ${task.number}: ${task.title}`);
        } else if (res.status === 400 || res.status === 401) {
          // Re-initialize session if expired
          console.log(`Session issue (status ${res.status}), re-initializing session...`);
          const reinit = await request('POST', '/mcp', {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/event-stream',
            'Authorization': `Bearer ${BONSAI_TOKEN}`
          }, initPayload);
          sessionId = reinit.headers['mcp-session-id'];
          await sleep(500);
        } else {
          console.log(`Status ${res.status} on ${task.number}, retrying in 1s...`);
          await sleep(1000);
        }
      } catch (err) {
        console.error(`Error on ${task.number}:`, err.message);
        await sleep(1000);
      }
    }

    if (!success) {
      failCount++;
      console.error(`❌ Failed to update ${task.number} after ${attempts} attempts.`);
    }

    // Gentle pacing (100ms) to respect rate limits
    await sleep(100);
  }

  console.log(`\n========================================`);
  console.log(`Update complete! Success: ${successCount}, Failed: ${failCount}`);
  console.log(`========================================\n`);

  fs.writeFileSync('scratch/updated_tasks_log.json', JSON.stringify(updatedList, null, 2));
}

run().catch(console.error);
