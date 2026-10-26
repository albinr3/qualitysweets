async function inspectCssRules() {
  const res = await fetch("https://qualitysweetsnj.com/carrot-halwa/");
  const html = await res.text();

  // Find linked CSS stylesheets
  const cssMatches = [...html.matchAll(/<link[^>]+rel=["']stylesheet["'][^>]+href=["']([^"']+)["']/gi)];
  console.log("Found stylesheets:", cssMatches.map(m => m[1]));

  for (const m of cssMatches) {
    const cssUrl = m[1].startsWith("http") ? m[1] : "https://qualitysweetsnj.com" + m[1];
    try {
      const cRes = await fetch(cssUrl);
      const cssText = await cRes.text();
      console.log(`\n=== STYLESHEET: ${cssUrl.split("/").pop()} (${cssText.length} bytes) ===`);
      
      const selectors = [
        "CategoryList h2",
        "PageMenu",
        "DrawerMenu",
        "BrandName",
        "rating_box",
        "SideCategoryList",
        "SidePopularProducts",
        "FooterUpper",
        "NewsletterSubscription"
      ];
      for (const sel of selectors) {
        const regex = new RegExp(`[^{}]*${sel}[^{}]*\\{[^}]*\\}`, "gi");
        const found = cssText.match(regex);
        if (found) {
          console.log(`Selectors matching "${sel}":`, found.slice(0, 3));
        }
      }
    } catch (err) {
      console.error("Error fetching", cssUrl, err.message);
    }
  }
}

inspectCssRules().catch(console.error);
