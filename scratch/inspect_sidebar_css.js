async function inspectSidebarCss() {
  const res = await fetch("https://qualitysweetsnj.com/carrot-halwa/");
  const html = await res.text();

  // Find all stylesheet links or inline styles
  const styles = [...html.matchAll(/<link[^>]+href=["']([^"']+\.css[^"']*)["']/gi)].map(m => m[1]);
  for (const s of styles) {
    const url = s.startsWith("http") ? s : "https://qualitysweetsnj.com" + s;
    const cRes = await fetch(url);
    const text = await cRes.text();
    const matches = text.match(/[^{}]*(?:\.Block\s+h2|\.Left\s+h2|SideCategoryList|SidePopularProducts|NewsletterSubscription)[^{}]*\{[^}]*\}/gi);
    if (matches) {
      console.log(`\n=== MATCHES IN ${url} ===`);
      matches.forEach(m => console.log(m.trim()));
    }
  }
}

inspectSidebarCss().catch(console.error);
