async function parseRealDomHeadings() {
  const res = await fetch("https://qualitysweetsnj.com/carrot-halwa/");
  let html = await res.text();

  // Strip scripts and styles
  html = html.replace(/<script[\s\S]*?<\/script>/gi, "");
  html = html.replace(/<style[\s\S]*?<\/style>/gi, "");

  const regex = /<(h[1-6])([^>]*)>([\s\S]*?)<\/\1>/gi;
  let match;
  console.log("=== ACTUAL RENDERED HEADINGS (EXCLUDING SCRIPTS/STYLES) ===");
  let count = 0;
  while ((match = regex.exec(html)) !== null) {
    count++;
    const tag = match[1].toUpperCase();
    const attrs = match[2];
    const text = match[3].replace(/<[^>]+>/g, "").trim().replace(/\s+/g, " ");
    console.log(`${count}. <${tag}> | text: "${text}" | attrs: [${attrs.trim()}]`);
  }
}

parseRealDomHeadings().catch(console.error);
