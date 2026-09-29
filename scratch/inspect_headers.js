async function inspectChildSitemaps() {
  const urls = [
    "https://qualitysweetsnj.com/xmlsitemap.php?type=pages&page=1",
    "https://qualitysweetsnj.com/xmlsitemap.php?type=categories&page=1",
    "https://qualitysweetsnj.com/xmlsitemap.php?type=news&page=1",
    "https://qualitysweetsnj.com/xmlsitemap.php?type=products&page=1"
  ];

  for (const u of urls) {
    const res = await fetch(u, {
      headers: {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5"
      }
    });
    console.log("=== URL:", u, "===");
    console.log("Status:", res.status, res.statusText);
    console.log("Content-Type:", res.headers.get("content-type"));
    console.log("Cache-Control:", res.headers.get("cache-control"));
    const txt = await res.text();
    console.log("Length:", txt.length);
    console.log("Start:", txt.slice(0, 80));
    console.log("End:", txt.slice(-80));
  }
}
inspectChildSitemaps();
