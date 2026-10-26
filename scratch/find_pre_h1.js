async function findPreH1() {
  const res = await fetch("https://qualitysweetsnj.com/carrot-halwa/");
  const html = await res.text();

  const h1Idx = html.indexOf("<h1");
  const preH1 = html.slice(0, h1Idx);

  console.log("=== PRE-H1 HTML HEADINGS ===");
  const regex = /<(h[1-6])([^>]*)>([\s\S]*?)<\/\1>/gi;
  let match;
  while ((match = regex.exec(preH1)) !== null) {
    console.log(`Tag: <${match[1]}> Attrs: [${match[2].trim()}] Content: "${match[3].trim()}"`);
    const pos = match.index;
    console.log("Context around heading:", preH1.slice(Math.max(0, pos - 100), Math.min(preH1.length, pos + 150)));
    console.log("-----------------------------------------");
  }
}

findPreH1().catch(console.error);
