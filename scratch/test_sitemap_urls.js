import fs from "fs";

async function testAllUrls() {
  const subSitemaps = [
    "https://qualitysweetsnj.com/xmlsitemap.php?type=pages&page=1",
    "https://qualitysweetsnj.com/xmlsitemap.php?type=products&page=1",
    "https://qualitysweetsnj.com/xmlsitemap.php?type=categories&page=1",
    "https://qualitysweetsnj.com/xmlsitemap.php?type=news&page=1"
  ];

  const allUrls = [];
  for (const s of subSitemaps) {
    const res = await fetch(s);
    const xml = await res.text();
    const locRegex = /<loc>(.*?)<\/loc>/g;
    let m;
    while ((m = locRegex.exec(xml)) !== null) {
      allUrls.push({ sitemap: s, url: m[1].trim() });
    }
  }

  console.log(`Total URLs found: ${allUrls.length}`);

  const results = [];
  const concurrency = 6;
  for (let i = 0; i < allUrls.length; i += concurrency) {
    const batch = allUrls.slice(i, i + concurrency);
    await Promise.all(
      batch.map(async (item) => {
        try {
          const r = await fetch(item.url, {
            method: "GET",
            redirect: "manual",
            headers: {
              "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
            }
          });
          const status = r.status;
          const location = r.headers.get("location");
          let canonical = null;
          let noindex = false;

          if (status === 200) {
            const body = await r.text();
            const cMatch = body.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["']/i);
            if (cMatch) {
              canonical = cMatch[1];
            }
            if (/noindex/i.test(body) && /meta[^>]+name=["']robots["'][^>]+content=["'][^"']*noindex/i.test(body)) {
              noindex = true;
            }
          }

          results.push({
            url: item.url,
            sitemap: item.sitemap,
            status,
            location,
            canonical,
            noindex
          });
        } catch (err) {
          results.push({
            url: item.url,
            sitemap: item.sitemap,
            status: `ERROR: ${err.message}`
          });
        }
      })
    );
    process.stdout.write(".");
  }

  console.log("\nDone scanning URLs!");
  fs.writeFileSync("scratch/sitemap_audit_results.json", JSON.stringify(results, null, 2));

  const redirects = results.filter((r) => [301, 302, 303, 307, 308].includes(r.status));
  const errors = results.filter((r) => typeof r.status === "number" && r.status >= 400);
  const exceptions = results.filter((r) => typeof r.status === "string" && r.status.startsWith("ERROR"));
  const noindexed = results.filter((r) => r.noindex);
  const canonicalMismatches = results.filter((r) => {
    if (!r.canonical) return false;
    // Normalize trailing slash
    const uNorm = r.url.replace(/\/$/, "");
    const cNorm = r.canonical.replace(/\/$/, "");
    return uNorm !== cNorm;
  });

  console.log("\n================ SUMMARY ================");
  console.log(`Total URLs: ${results.length}`);
  console.log(`200 OK: ${results.filter((r) => r.status === 200).length}`);
  console.log(`Redirects (3xx): ${redirects.length}`);
  console.log(`Errors (4xx / 5xx): ${errors.length}`);
  console.log(`Fetch Exceptions: ${exceptions.length}`);
  console.log(`Noindexed: ${noindexed.length}`);
  console.log(`Canonical Mismatches: ${canonicalMismatches.length}`);

  if (redirects.length > 0) {
    console.log("\n--- REDIRECTS ---");
    console.log(JSON.stringify(redirects, null, 2));
  }
  if (errors.length > 0) {
    console.log("\n--- ERRORS ---");
    console.log(JSON.stringify(errors, null, 2));
  }
  if (canonicalMismatches.length > 0) {
    console.log("\n--- CANONICAL MISMATCHES ---");
    console.log(JSON.stringify(canonicalMismatches, null, 2));
  }
  if (noindexed.length > 0) {
    console.log("\n--- NOINDEXED ---");
    console.log(JSON.stringify(noindexed, null, 2));
  }
}

testAllUrls().catch(console.error);
