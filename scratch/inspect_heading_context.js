async function inspectContext() {
  const res = await fetch("https://qualitysweetsnj.com/carrot-halwa/");
  const html = await res.text();

  const headings = [
    "Shop",
    "Visit &amp; Order",
    "About &amp; Help",
    "Categories",
    "BrandName",
    "Write Your Own Review",
    "Popular Products",
    "Sign up to our newsletter",
    "Contact Us",
    "Connect with us",
    "Information"
  ];

  for (const h of headings) {
    const idx = html.indexOf(h);
    if (idx !== -1) {
      console.log(`\n=== CONTEXT FOR "${h}" ===`);
      console.log(html.slice(Math.max(0, idx - 150), Math.min(html.length, idx + 150)));
    }
  }
}

inspectContext().catch(console.error);
