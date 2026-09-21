const https = require('https');
const fs = require('fs');

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

async function run() {
  const initPayload = JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'initialize',
    params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'sync', version: '1.0' } }
  });

  const res1 = await request('POST', '/mcp', {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/event-stream',
    'Authorization': 'Bearer bonsai_at_6DmXce5_xF66dEgF5_B1cHlJnk6O_-UHXhUcYi3Ztv8'
  }, initPayload);

  const sessionId = res1.headers['mcp-session-id'];
  if (!sessionId) {
    console.error('Failed to get session ID:', res1.body);
    return;
  }

  let allTasks = [];
  let page = 1;
  let hasMore = true;

  while (hasMore) {
    const callPayload = JSON.stringify({
      jsonrpc: '2.0',
      id: page + 1,
      method: 'tools/call',
      params: {
        name: 'list_tasks',
        arguments: {
          project_id: 1535714,
          scope: 'all',
          page_size: 100,
          page: page
        }
      }
    });

    const res2 = await request('POST', '/mcp', {
      'Content-Type': 'application/json',
      'Accept': 'application/json, text/event-stream',
      'Authorization': 'Bearer bonsai_at_6DmXce5_xF66dEgF5_B1cHlJnk6O_-UHXhUcYi3Ztv8',
      'Mcp-Session-Id': sessionId
    }, callPayload);

    const line = res2.body.split('\n').find(l => l.startsWith('data: '));
    if (!line) {
      console.error('No data line on page', page, res2.body);
      break;
    }
    const parsed = JSON.parse(line.substring(6));
    const tasks = parsed.result.structuredContent.tasks || [];
    allTasks = allTasks.concat(tasks);
    hasMore = parsed.result.structuredContent.pagination.has_more;
    console.log(`Page ${page}: ${tasks.length} tasks (total: ${allTasks.length})`);
    page++;
  }

  fs.writeFileSync('scratch/bonsai_tasks.json', JSON.stringify(allTasks, null, 2));
  console.log(`Successfully saved ${allTasks.length} tasks to scratch/bonsai_tasks.json`);
}

run().catch(console.error);
