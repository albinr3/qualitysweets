async function checkSitemap() {
  const res = await fetch("https://qualitysweetsnj.com/xmlsitemap.php");
  console.log("Sitemap status:", res.status);
  const text = await res.text();
  console.log("Sitemap length:", text.length);
  
  const urls = [
    "carrot-halwa",
    "plain-burfi",
    "kaju-katli",
    "motichur-ladoo",
    "besan-ladoo",
    "gulab-jamoon-large",
    "rasgulla-large",
    "moong-dal-halwa",
    "imarti",
    "milk-cake"
  ];

  for (const u of urls) {
    const idx = text.indexOf(u);
    if (idx !== -1) {
      const chunk = text.slice(Math.max(0, idx - 60), Math.min(text.length, idx + 120));
      console.log(`FOUND ${u}:\n`, chunk.trim());
      console.log("-----------------------------------------");
    } else {
      console.log(`NOT FOUND in sitemap: ${u}`);
    }
  }
}

checkSitemap().catch(console.error);
