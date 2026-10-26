const urls = [
  { id: 112, name: "Plain Burfi", url: "https://qualitysweetsnj.com/plain-burfi/", expectedTitle: "Plain Burfi (Mawa Barfi)" },
  { id: 77, name: "Kaju Katli", url: "https://qualitysweetsnj.com/kaju-katli/", expectedTitle: "Kaju Katli (Kaju Barfi)" },
  { id: 104, name: "Motichur Ladoo", url: "https://qualitysweetsnj.com/motichur-ladoo/", expectedTitle: "Motichur Ladoo (Motichoor Laddu)" },
  { id: 98, name: "Besan Ladoo", url: "https://qualitysweetsnj.com/besan-ladoo/", expectedTitle: "Besan Ladoo (Besan Ke Laddu)" },
  { id: 127, name: "Gulab Jamoon", url: "https://qualitysweetsnj.com/gulab-jamoon-large/", expectedTitle: "Gulab Jamun (Gulab Jamoon)" },
  { id: 126, name: "Rasgulla", url: "https://qualitysweetsnj.com/rasgulla-large/", expectedTitle: "Rasgulla (Roshogolla)" },
  { id: 92, name: "Moong Dal Halwa", url: "https://qualitysweetsnj.com/moong-dal-halwa/", expectedTitle: "Moong Dal Halwa" },
  { id: 94, name: "Imarti", url: "https://qualitysweetsnj.com/imarti/", expectedTitle: "Imarti (Amriti / Jahangir)" },
  { id: 105, name: "Milk Cake", url: "https://qualitysweetsnj.com/milk-cake/", expectedTitle: "Milk Cake (Alwar Ka Mawa)" }
];

async function verifyAllLive() {
  console.log("=== VERIFYING ALL 9 LIVE PRODUCT URLS ===\n");
  let allPassed = true;

  for (const item of urls) {
    try {
      const res = await fetch(item.url, { headers: { "Cache-Control": "no-cache" } });
      const html = await res.text();

      const titleMatch = html.match(/<title>([^<]+)<\/title>/i);
      const title = titleMatch ? titleMatch[1].trim() : "NOT FOUND";

      const metaMatch = html.match(/<meta\s+name=["']description["']\s+content=["']([^"']+)["']/i);
      const meta = metaMatch ? metaMatch[1].trim() : "NOT FOUND";

      const hasContent = html.includes("qs-product-content-wrapper");
      const hasSchema = html.includes(`qs-schema-product-${item.id}-v2`);

      const schemaRegex = new RegExp(`<script type="application/ld\\+json" id="qs-schema-product-${item.id}-v2">([\\s\\S]*?)<\\/script>`, "i");
      const schemaMatch = html.match(schemaRegex);
      let schemaValid = false;
      let brand = "";
      let diet = "";
      if (schemaMatch) {
        try {
          const parsed = JSON.parse(schemaMatch[1]);
          schemaValid = true;
          brand = parsed.brand?.name || "";
          diet = parsed.suitableForDiet || "";
        } catch (e) {
          schemaValid = false;
        }
      }

      const passed = res.status === 200 && title.includes(item.expectedTitle) && meta.length > 50 && hasContent && schemaValid;

      console.log(`[${passed ? "PASSED" : "FAILED"}] ID ${item.id} - ${item.name}`);
      console.log(`  URL: ${item.url}`);
      console.log(`  Status: ${res.status}`);
      console.log(`  Title (${title.length} ch): ${title}`);
      console.log(`  Meta  (${meta.length} ch): ${meta.slice(0, 80)}...`);
      console.log(`  Enriched HTML: ${hasContent ? "YES" : "NO"} | Schema v2: ${schemaValid ? `YES (Brand: ${brand}, Diet: ${diet})` : "NO"}`);
      console.log("-------------------------------------------------");

      if (!passed) allPassed = false;
    } catch (err) {
      console.error(`Error fetching ${item.url}:`, err.message);
      allPassed = false;
    }
  }

  console.log(`\nOVERALL BATCH VERIFICATION: ${allPassed ? "100% SUCCESS" : "SOME CHECKS FAILED"}`);
}

verifyAllLive().catch(console.error);
