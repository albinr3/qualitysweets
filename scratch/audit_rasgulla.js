async function auditRasgulla() {
  const url = "https://qualitysweetsnj.com/rasgulla-large/";
  console.log(`Fetching ${url}...`);
  const res = await fetch(url, { headers: { "Cache-Control": "no-cache", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" } });
  const html = await res.text();

  console.log(`HTTP Status: ${res.status}`);
  console.log(`Content-Type: ${res.headers.get("content-type")}`);

  // 1. Title & Meta
  const titleMatch = html.match(/<title>([^<]+)<\/title>/i);
  const title = titleMatch ? titleMatch[1].trim() : "";
  console.log(`\n--- TITLE & META ---`);
  console.log(`Title (${title.length} ch): "${title}"`);

  const metaMatch = html.match(/<meta\s+name=["']description["']\s+content=["']([^"']+)["']/i);
  const meta = metaMatch ? metaMatch[1].trim() : "";
  console.log(`Meta Description (${meta.length} ch): "${meta}"`);

  const canonicalMatch = html.match(/<link\s+rel=["']canonical["']\s+href=["']([^"']+)["']/i);
  console.log(`Canonical: ${canonicalMatch ? canonicalMatch[1] : "NONE"}`);

  const robotsMatch = html.match(/<meta\s+name=["']robots["']\s+content=["']([^"']+)["']/i);
  console.log(`Robots: ${robotsMatch ? robotsMatch[1] : "NONE (defaults to index, follow)"}`);

  // 2. Open Graph & Social
  console.log(`\n--- OPEN GRAPH ---`);
  const ogTitle = html.match(/<meta\s+property=["']og:title["']\s+content=["']([^"']+)["']/i);
  const ogDesc = html.match(/<meta\s+property=["']og:description["']\s+content=["']([^"']+)["']/i);
  const ogImage = html.match(/<meta\s+property=["']og:image["']\s+content=["']([^"']+)["']/i);
  console.log(`og:title: ${ogTitle ? ogTitle[1] : "NONE"}`);
  console.log(`og:image: ${ogImage ? ogImage[1] : "NONE"}`);

  // 3. Headings in Raw HTML
  console.log(`\n--- HEADINGS IN RAW HTML ---`);
  const cleanHtml = html.replace(/<script[\s\S]*?<\/script>/gi, "").replace(/<style[\s\S]*?<\/style>/gi, "");
  const headingRegex = /<(h[1-6])([^>]*)>([\s\S]*?)<\/\1>/gi;
  let hMatch;
  const headings = [];
  while ((hMatch = headingRegex.exec(cleanHtml)) !== null) {
    headings.push({
      tag: hMatch[1].toUpperCase(),
      attrs: hMatch[2].trim(),
      text: hMatch[3].replace(/<[^>]+>/g, "").trim().replace(/\s+/g, " ")
    });
  }
  headings.forEach((h, i) => {
    console.log(`${i + 1}. <${h.tag}> "${h.text}" [attrs: ${h.attrs}]`);
  });

  // 4. Schema.org JSON-LD
  console.log(`\n--- STRUCTURED DATA (SCHEMA.ORG) ---`);
  const schemaRegex = /<script\s+type=["']application\/ld\+json["']([^>]*)>([\s\S]*?)<\/script>/gi;
  let sMatch;
  let schemaCount = 0;
  while ((sMatch = schemaRegex.exec(html)) !== null) {
    schemaCount++;
    console.log(`Schema Block ${schemaCount} (attrs: ${sMatch[1]}):`);
    try {
      const parsed = JSON.parse(sMatch[2]);
      console.log(JSON.stringify(parsed, null, 2));
    } catch (err) {
      console.log(`Invalid JSON: ${err.message}`);
    }
  }

  // 5. Content Analysis
  console.log(`\n--- CONTENT QUALITY & E-E-A-T ---`);
  const wrapperIdx = html.indexOf("qs-product-content-wrapper");
  if (wrapperIdx !== -1) {
    const wrapperChunk = html.slice(wrapperIdx, wrapperIdx + 4000);
    const textOnly = wrapperChunk.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");
    const words = textOnly.trim().split(" ").length;
    console.log(`Product Content Words: ~${words}`);
    console.log(`Contains Em Dash (—): ${wrapperChunk.includes("—")}`);
    console.log(`Contains Freshness / Serving Guide: ${wrapperChunk.includes("Serving &amp; Reheating Tips") || wrapperChunk.includes("Serving")}`);
    console.log(`Contains FAQs: ${wrapperChunk.includes("Frequently Asked Questions")}`);
  } else {
    console.log("qs-product-content-wrapper NOT FOUND!");
  }

  // 6. Primary Image
  console.log(`\n--- PRIMARY IMAGE ---`);
  const imgRegex = /<img[^>]+src=["']([^"']+)["'][^>]*alt=["']([^"']*)["'][^>]*>/gi;
  let imgMatch;
  while ((imgMatch = imgRegex.exec(html)) !== null) {
    if (imgMatch[1].includes("Big_Rasgulla") || imgMatch[1].includes("/products/126/")) {
      console.log(`Product Image src: ${imgMatch[1]}`);
      console.log(`Product Image alt: "${imgMatch[2]}"`);
    }
  }
}

auditRasgulla().catch(console.error);
