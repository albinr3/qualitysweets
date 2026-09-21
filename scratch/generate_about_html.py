import json

html_content = """<style>
  .TitleHeading { display: none !important; }
  .qs-about {
    font-family: Arial, sans-serif;
    color: #361018;
    max-width: 1180px;
    margin: 0 auto;
    padding: 18px 14px 42px;
    line-height: 1.65;
    box-sizing: border-box;
  }
  .qs-about * { box-sizing: border-box; }
  .qs-about h1, .qs-about h2, .qs-about h3 {
    font-family: Georgia, serif;
    color: #701326;
    line-height: 1.25;
  }
  .qs-about h1 {
    font-size: clamp(28px, 4vw, 44px);
    margin: 8px 0 14px;
    color: #ffffff;
  }
  .qs-about h2 {
    font-size: clamp(22px, 3vw, 30px);
    margin: 0 0 14px;
  }
  .qs-about h3 {
    font-size: 20px;
    margin: 0 0 8px;
  }
  .qs-about p {
    font-size: 16px;
    margin: 0 0 16px;
  }
  .qs-about p:last-child {
    margin-bottom: 0;
  }
  .qs-hero {
    background: linear-gradient(135deg, #4b0714, #87182d);
    border: 2px solid #d7b35a;
    border-radius: 14px;
    color: #ffffff;
    padding: clamp(28px, 5vw, 52px);
    text-align: center;
  }
  .qs-kicker {
    color: #ffd878;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .qs-hero p {
    color: #ffefd5;
    max-width: 820px;
    margin: 0 auto 24px;
    font-size: 17px;
  }
  .qs-actions {
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
  }
  .qs-btn {
    background: #ffffff;
    color: #701326 !important;
    border-radius: 6px;
    display: inline-block;
    font-weight: 700;
    padding: 12px 20px;
    text-decoration: none;
    transition: background 0.2s ease, transform 0.1s ease;
  }
  .qs-btn:hover {
    background: #f7ede2;
  }
  .qs-btn--gold {
    background: #d7b35a;
    color: #3b0b14 !important;
  }
  .qs-btn--gold:hover {
    background: #c69e46;
  }
  .qs-section {
    margin-top: 28px;
    padding: 28px;
    background: #fffdf9;
    border: 1px solid #eadfcb;
    border-radius: 12px;
    box-shadow: 0 3px 14px rgba(58, 17, 24, 0.05);
  }
  .qs-photo-grid {
    display: grid;
    gap: 20px;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .qs-photo {
    margin: 0;
  }
  .qs-photo img {
    display: block;
    width: 100%;
    height: 330px;
    object-fit: cover;
    border-radius: 9px;
  }
  .qs-photo figcaption {
    color: #6a5556;
    font-size: 13px;
    margin-top: 8px;
  }
  .qs-cards-grid {
    display: grid;
    gap: 20px;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    margin-top: 18px;
  }
  .qs-card {
    background: #ffffff;
    border: 1px solid #eadfcb;
    border-radius: 9px;
    padding: 20px;
  }
  .qs-card h3 {
    margin-top: 0;
    color: #701326;
  }
  .qs-card p {
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 12px;
  }
  .qs-card a.qs-card-link {
    font-weight: 700;
    color: #701326;
    text-decoration: underline;
    font-size: 14px;
  }
  .qs-detail-grid {
    display: grid;
    gap: 20px;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .qs-details {
    background: #fff6e7;
    border-left: 5px solid #d7b35a;
    border-radius: 7px;
    padding: 22px;
  }
  .qs-details p {
    margin-bottom: 12px;
  }
  .qs-map {
    border: 0;
    border-radius: 9px;
    min-height: 340px;
    width: 100%;
  }
  .qs-highlight-box {
    background: #fff5dc;
    border: 1px solid #d7b35a;
    border-radius: 9px;
    padding: 16px 20px;
    margin-top: 18px;
  }
  .qs-highlight-box strong {
    color: #701326;
  }
  @media (max-width: 720px) {
    .qs-photo-grid, .qs-cards-grid, .qs-detail-grid {
      grid-template-columns: 1fr;
    }
    .qs-photo img {
      height: 270px;
    }
    .qs-section {
      padding: 20px 16px;
    }
  }
</style>

<main class="qs-about">
  <section class="qs-hero">
    <div class="qs-kicker">Oak Tree Road &bull; Iselin, New Jersey &bull; Established 2003</div>
    <h1>About Quality Sweets</h1>
    <p>Authentic Bengali mithai, traditional Indian sweets, and fresh savory snacks handcrafted on Oak Tree Road in Iselin, New Jersey since 2003.</p>
    <div class="qs-actions">
      <a class="qs-btn qs-btn--gold" href="/indian-sweets/">Order Sweets Online</a>
      <a class="qs-btn" href="/menu/">View Takeout Menu</a>
      <a class="qs-btn" href="tel:+17322833799">Call (732) 283-3799</a>
    </div>
  </section>

  <section class="qs-section">
    <div class="qs-photo-grid">
      <figure class="qs-photo">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/410/quality-sweets-iselin-storefront-oak-tree-road__61587.1789245785.1280.1280.jpg?c=2" alt="Quality Sweets storefront at 1384 Oak Tree Road in Iselin, New Jersey" width="900" height="1020" fetchpriority="high">
        <figcaption>Our storefront at 1384 Oak Tree Road in Iselin, NJ.</figcaption>
      </figure>
      <figure class="qs-photo">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/411/quality-sweets-iselin-mithai-counter__70430.1789245787.1280.1280.jpg?c=2" alt="Fresh Indian mithai display counter at Quality Sweets on Oak Tree Road" width="900" height="1018" loading="lazy" decoding="async">
        <figcaption>Fresh daily sweet counter in Iselin, NJ.</figcaption>
      </figure>
    </div>
  </section>

  <section class="qs-section">
    <h2>Our Story on Oak Tree Road</h2>
    <p>Quality Sweets opened on Oak Tree Road in Iselin, New Jersey in 2003. When we started, fresh Bengali mithai was hard to find in the Tri-State area, so we built our kitchen around traditional recipes made with fresh milk, chhena, and pure desi ghee.</p>
    <p>More than twenty years later, we still make our sweets every morning at the exact same location.</p>
    <p>What began as a neighborhood confectionery serving local families in Middlesex County has grown to serve customers across New Jersey, New York, Pennsylvania, and through nationwide delivery. Through that entire period, our commitment to small-batch preparation and authentic regional flavors has remained unchanged.</p>
  </section>

  <section class="qs-section">
    <h2>Bengali Specialties &amp; Traditional Mithai</h2>
    <p>Our sweet makers from Bengal and Punjab prepare regional recipes from across India. Bengal is known for chhena-based sweets with delicate milk syrup, while northern regions are celebrated for rich cashew, pistachio, and gram-flour preparations. We honor both traditions daily in our kitchen.</p>

    <div class="qs-cards-grid">
      <div class="qs-card">
        <h3>Signature Bengali Sweets</h3>
        <p>Our counter is famous for classic Bengali confections made from freshly curdled milk (chhena). Popular choices include <a href="/manpasand/">Manpasand</a>, <a href="/anarkali/">Anarkali</a>, <a href="/malai-chum-chum/">Malai Chum Chum</a>, and <a href="/palki/">Palki</a>, alongside classic Rasgulla and Sandesh.</p>
        <a class="qs-card-link" href="/bengali-sweets/">Explore Bengali Sweets &rarr;</a>
      </div>

      <div class="qs-card">
        <h3>Traditional Indian Mithai</h3>
        <p>We prepare classic sweets for daily enjoyment and festival celebrations, including diamond-cut <a href="/barfi/">Kaju Katli</a>, Motichur Ladoos, Gulab Jamun, Besan Barfi, and Pistachio Roll. Each batch is made in small batches to preserve texture and flavor.</p>
        <a class="qs-card-link" href="/traditional-mithai/">Browse Traditional Mithai &rarr;</a>
      </div>

      <div class="qs-card">
        <h3>Hot Samosas &amp; Fresh Chaat</h3>
        <p>In addition to sweet confections, our counter serves hot, freshly prepared Indian street snacks for takeout: crisp potato-and-pea samosas, samosa chaat, dahi bhalla, pani puri, and chole bhatura.</p>
        <a class="qs-card-link" href="/menu/">See Takeout Menu &rarr;</a>
      </div>

      <div class="qs-card">
        <h3>Mithai Gift Boxes &amp; Catering</h3>
        <p>We pack custom sweet assortments for weddings, corporate celebrations, temple prasad, and Diwali gifts. Choose your favorite sweets by the pound or arrange large orders for private events.</p>
        <a class="qs-card-link" href="/catering/">Learn About Catering &rarr;</a>
      </div>
    </div>
  </section>

  <section class="qs-section">
    <h2>Pure Ingredients, Traditional Methods</h2>
    <p>Authentic Indian sweets depend on the quality of their milk and fat. We do not cut corners with premixed powders, food gums, or artificial preservatives.</p>
    <p>Our kitchen relies on whole dairy milk, pure desi ghee, fresh unadulterated khoya, green cardamom, cashews, almonds, and saffron. Every confection we prepare is 100% vegetarian.</p>
    <div class="qs-highlight-box">
      <strong>Vegetarian Guarantee:</strong> All Quality Sweets products are strictly vegetarian, made without gelatin, animal fats, or eggs.
    </div>
  </section>

  <section class="qs-section">
    <h2>Visit Us in Iselin, NJ &bull; Store Hours &amp; Pickup</h2>
    <div class="qs-detail-grid">
      <div class="qs-details">
        <h3>Quality Sweets</h3>
        <p><strong>Address:</strong><br>1384 Oak Tree Road<br>Iselin, NJ 08830<br><em>Located on Oak Tree Road bordering Edison</em></p>
        <p><strong>Phone:</strong> <a href="tel:+17322833799">(732) 283-3799</a><br><strong>WhatsApp:</strong> <a href="https://wa.me/17328037617" target="_blank" rel="noopener">(732) 803-7617</a></p>
        <p><strong>Hours:</strong><br>Monday &ndash; Sunday: 10:00 AM &ndash; 8:00 PM<br>Open seven days a week</p>
        <p><strong>Service Type:</strong> Counter pickup and takeout. Customer parking is available behind our building.</p>
        <p>
          <a class="qs-btn qs-btn--gold" href="https://maps.app.goo.gl/CxdRcdqp4ikhE7wd7" target="_blank" rel="noopener">Get Driving Directions</a>
        </p>
      </div>
      <iframe class="qs-map" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3030.535200747086!2d-74.3261661!3d40.573940400000005!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c3b68fb2ee8561%3A0xd62bfc7899a9913c!2sQuality%20Sweets%20-%20Indian%20Sweets%20Shop!5e0!3m2!1sen!2sdo!4v1789957879487!5m2!1sen!2sdo" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" title="Quality Sweets - Indian Sweets Shop on Google Maps"></iframe>
    </div>
  </section>
</main>

<script>
  (function () {
    function replaceWithDiv(node) {
      var replacement = document.createElement('div');
      for (var i = 0; i < node.attributes.length; i += 1) {
        replacement.setAttribute(node.attributes[i].name, node.attributes[i].value);
      }
      replacement.className += ' qs-nonheading-label';
      replacement.innerHTML = node.innerHTML;
      node.parentNode.replaceChild(replacement, node);
    }

    Array.prototype.slice.call(document.querySelectorAll('h2')).forEach(function (heading) {
      if (heading.textContent.trim().toLowerCase() === 'categories') replaceWithDiv(heading);
    });
    Array.prototype.slice.call(document.querySelectorAll('h1')).forEach(function (heading) {
      if (heading.textContent.trim() === 'About Us' || heading.classList.contains('TitleHeading')) heading.remove();
    });
  }());
</script>

<script id="qs-schema-about-v1" type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "AboutPage",
  "@id": "https://qualitysweetsnj.com/about-us#webpage",
  "url": "https://qualitysweetsnj.com/about-us",
  "name": "About Quality Sweets | Handcrafted Indian Mithai Since 2003",
  "description": "Quality Sweets has been handcrafting authentic Bengali mithai and traditional Indian sweets on Oak Tree Road in Iselin, NJ since 2003.",
  "mainEntity": {
    "@type": "Bakery",
    "@id": "https://qualitysweetsnj.com/#business",
    "name": "Quality Sweets",
    "image": "https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/410/quality-sweets-iselin-storefront-oak-tree-road__61587.1789245785.1280.1280.jpg?c=2",
    "telephone": "+1-732-283-3799",
    "priceRange": "$$",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "1384 Oak Tree Road",
      "addressLocality": "Iselin",
      "addressRegion": "NJ",
      "postalCode": "08830",
      "addressCountry": "US"
    },
    "openingHoursSpecification": [
      {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "opens": "10:00",
        "closes": "20:00"
      }
    ],
    "servesCuisine": "Indian",
    "foundingDate": "2003"
  }
}
</script>
"""

with open("scratch/about_page_new.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Saved scratch/about_page_new.html")
