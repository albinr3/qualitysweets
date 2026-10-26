async function checkLive() {
  try {
    const res = await fetch("https://qualitysweetsnj.com/carrot-halwa/", {
      headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
    });
    console.log("Status:", res.status);
    const html = await res.text();
    
    const titleMatch = html.match(/<title>([^<]+)<\/title>/i);
    const metaMatch = html.match(/<meta\s+name=["']description["']\s+content=["']([^"']*)["']/i);
    const hasWrapper = html.includes("qs-product-content-wrapper");
    const hasSchema = html.includes("qs-schema-product-93-v2");

    console.log("--- RESULTADOS EN VIVO ---");
    console.log("Title Tag:", titleMatch ? titleMatch[1] : "NO ENCONTRADO");
    console.log("Meta Description:", metaMatch ? metaMatch[1] : "NO ENCONTRADO");
    console.log("Contenido Enriquecido Presente:", hasWrapper);
    console.log("Schema JSON-LD v2 Presente:", hasSchema);

    // Extract Schema JSON
    const schemaMatch = html.match(/<script\s+id=["']qs-schema-product-93-v2["'][^>]*>([\s\S]*?)<\/script>/i);
    if (schemaMatch) {
      try {
        const parsed = JSON.parse(schemaMatch[1]);
        console.log("Schema JSON Valido: SI");
        console.log("Brand:", parsed.brand?.name);
        console.log("Alternate Names:", parsed.alternateName);
        console.log("Diet:", parsed.suitableForDiet);
        console.log("Offer Price:", parsed.offers?.price, parsed.offers?.priceCurrency);
        console.log("Offer Shipping:", parsed.offers?.shippingDetails ? "SI" : "NO");
      } catch (e) {
        console.error("Error parseando Schema JSON:", e.message);
      }
    }
  } catch (err) {
    console.error("Error al consultar web en vivo:", err);
  }
}

checkLive();
