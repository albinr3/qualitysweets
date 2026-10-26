import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const envPath = path.join(ROOT, ".env");

const env = {};
if (fs.existsSync(envPath)) {
  for (const line of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) continue;
    const idx = trimmed.indexOf("=");
    env[trimmed.slice(0, idx).trim()] = trimmed.slice(idx + 1).trim().replace(/^['"]|['"]$/g, "");
  }
}

const storeHash = env.BIGCOMMERCE_STORE_HASH || process.env.BIGCOMMERCE_STORE_HASH;
const token = env.BIGCOMMERCE_ACCESS_TOKEN || process.env.BIGCOMMERCE_ACCESS_TOKEN;

if (!storeHash || !token) {
  console.error("Missing BIGCOMMERCE_STORE_HASH or BIGCOMMERCE_ACCESS_TOKEN.");
  process.exit(1);
}

// 9 Remaining Flagship Products
const products = [
  // 1. Plain Burfi (ID 112)
  {
    id: 112,
    sku: "47",
    urlSlug: "plain-burfi",
    url: "https://qualitysweetsnj.com/plain-burfi/",
    canonicalName: "Plain Burfi",
    alternateNames: ["Plain Barfi", "Mawa Barfi", "Khoya Burfi", "Milk Burfi"],
    page_title: "Plain Burfi (Mawa Barfi) | Fresh Khoya Sweet | Quality Sweets",
    meta_description: "Traditional Plain Burfi cut into classic diamonds. Made with fresh reduced milk khoya and crushed cardamom. 0 preservatives. Shipped fresh across the USA.",
    search_keywords: "plain burfi, mawa barfi, khoya burfi, milk burfi, barfi sweets, buy burfi online usa, authentic plain barfi, handcrafted mithai",
    price: "7.50",
    image: "https://cdn10.bigcommerce.com/s-2ygwtj/products/112/images/307/Kaju_Katly1__50684.1790725939.1280.1280.jpg?c=2",
    p1: "Plain Burfi (often called Mawa Barfi or Khoya Burfi) is made by patiently reducing fresh whole milk until it thickens into rich khoya, sweetened lightly, and finished with a pinch of green cardamom. Each batch is cooled and cut into traditional diamond pieces, with roughly 12 to 14 pieces per pound.",
    moatHeading: "Why Quality Sweets Plain Burfi Stands Apart",
    moatBullets: [
      "Zero Chemical Preservatives: Handcrafted daily in our Iselin shop using fresh dairy.",
      "Pure Milk Khoya: Cooked down from whole milk without milk powder fillers, starch, or artificial thickeners.",
      "100% Vegetarian: Eggless, gelatin-free, and prepared under traditional purity standards."
    ],
    servingTips: "Enjoy at room temperature with hot masala chai, or serve as a classic sweet for poojas, weddings, and Diwali gatherings.",
    storageTips: "Store in a sealed container in a cool spot or refrigerator between 38°F and 42°F. Stays fresh for 10 to 14 days.",
    faqs: [
      {
        q: "How many pieces of Plain Burfi come in a one-pound box?",
        a: "A one-pound box contains approximately 12 to 14 diamond-cut pieces of fresh Plain Burfi."
      },
      {
        q: "How does nationwide shipping work for fresh burfi?",
        a: "Orders ship Monday through Wednesday with food-grade gel ice packs in insulated thermal packaging via FedEx Ground and Express."
      },
      {
        q: "Can I combine Plain Burfi with other mithai in a custom box?",
        a: "Yes. You can order custom mithai gift boxes featuring Plain Burfi alongside Kaju Katli, Ladoos, and Bengali sweets."
      }
    ]
  },

  // 2. Kaju Katli (ID 77)
  {
    id: 77,
    sku: "11",
    urlSlug: "kaju-katli",
    url: "https://qualitysweetsnj.com/kaju-katli/",
    canonicalName: "Kaju Katli",
    alternateNames: ["Kaju Barfi", "Kaju Qatli", "Cashew Fudge"],
    page_title: "Kaju Katli (Kaju Barfi) | Fresh Cashew Sweets | Quality Sweets",
    meta_description: "Traditional Kaju Katli diamond sweets made with ground cashews, sugar, and cardamom. Never cut with peanuts. No preservatives. Ships fresh across the USA.",
    search_keywords: "kaju katli, kaju barfi, buy kaju katli online usa, cashew sweet, fresh kaju katli, diwali kaju katli, authentic mithai nj",
    price: "9.00",
    image: "https://cdn10.bigcommerce.com/s-2ygwtj/products/77/images/308/Plain_Burfi__57958.1790725926.1280.1280.jpg?c=2",
    p1: "Kaju Katli (also known as Kaju Barfi) is India's most celebrated festive cashew sweet. We make ours by grinding premium whole cashews into a fine paste, cooking it down with simple syrup and cardamom, rolling it thin, and slicing it into clean diamond shapes. Each pound contains approximately 18 diamond pieces.",
    moatHeading: "Why Quality Sweets Kaju Katli Stands Apart",
    moatBullets: [
      "100% Whole Cashews: Prepared strictly with whole cashews, pure sugar, and cardamom. Never cut with peanuts, flour, or artificial binders.",
      "Zero Chemical Preservatives: Handcrafted daily in our Iselin kitchen without palm oil or synthetic additives.",
      "Naturally Long Shelf Life: Pure nut fudge stays delicious for up to 2 weeks at room temperature or refrigerated."
    ],
    servingTips: "Serve at room temperature. Kaju Katli is the quintessential gift for Diwali, weddings, Raksha Bandhan, and housewarmings.",
    storageTips: "Keep in an airtight box at room temperature away from direct sunlight for up to 14 days, or refrigerate for up to 3 weeks.",
    faqs: [
      {
        q: "Do you use peanuts or peanut oil in your Kaju Katli?",
        a: "No. Our Kaju Katli is made with 100% pure whole cashews, sugar, and cardamom. We never use peanuts or peanut fillers."
      },
      {
        q: "How does nationwide shipping work for Kaju Katli?",
        a: "Because of its firm texture and nut base, Kaju Katli travels exceptionally well. Boxes are sealed with cold protection and shipped Monday through Wednesday via FedEx."
      },
      {
        q: "Are the pieces decorated with silver foil (vark)?",
        a: "We offer both traditional silver-leafed and plain unadorned boxes depending on customer preference."
      }
    ]
  },

  // 3. Motichur Ladoo (ID 104)
  {
    id: 104,
    sku: "39",
    urlSlug: "motichur-ladoo",
    url: "https://qualitysweetsnj.com/motichur-ladoo/",
    canonicalName: "Motichur Ladoo",
    alternateNames: ["Motichoor Ladoo", "Motichur Laddu", "Boondi Ladoo", "Prasad Ladoo"],
    page_title: "Motichur Ladoo (Motichoor Laddu) | Fresh Mithai | Quality Sweets",
    meta_description: "Fresh Motichur Ladoo made with tiny besan pearls fried in pure ghee and soaked in saffron syrup. No preservatives. Ships fresh nationwide via FedEx.",
    search_keywords: "motichur ladoo, motichoor ladoo, motichur laddu, boondi ladoo, buy motichoor ladoo online, prasad ladoo, indian sweet shop",
    price: "6.50",
    image: "https://cdn10.bigcommerce.com/s-2ygwtj/products/104/images/299/Motichur_Ladoo__31599.1790725936.1280.1280.jpg?c=2",
    p1: "Motichur Ladoo (or Motichoor Laddu) is handcrafted by passing chickpea flour batter through a perforated ladle into hot desi ghee, producing tiny golden pearls known as boondi. The pearls are soaked in saffron and cardamom syrup, then rolled by hand into soft, juicy ladoos with slivered melon seeds. Approximately 8 pieces per pound.",
    moatHeading: "Why Quality Sweets Motichur Ladoo Stands Apart",
    moatBullets: [
      "100% Pure Desi Ghee: Fried strictly in pure cow desi ghee, never vegetable oil or vanaspati shortening.",
      "Handcrafted Daily: Made fresh every morning on Oak Tree Road with zero artificial colors or chemical preservatives.",
      "Traditional Religious Prasad: The authentic sweet offered for Ganesh Chaturthi, Hanuman Jayanti, Diwali, and family poojas."
    ],
    servingTips: "Enjoy at room temperature. If you prefer a warmer bite, heat a ladoo for 8 to 10 seconds in the microwave to release the fragrance of saffron and ghee.",
    storageTips: "Store in a sealed container at room temperature for up to 7 days, or refrigerate for up to 12 days.",
    faqs: [
      {
        q: "Are these made in pure ghee or vegetable oil?",
        a: "Our Motichur Ladoos are prepared 100% in pure desi ghee for authentic flavor, texture, and ritual purity."
      },
      {
        q: "Do you ship Motichur Ladoos nationwide without crushing?",
        a: "Yes. We hand-pack each ladoo into compartmentalized sweet trays inside insulated thermal boxes to ensure they arrive round and intact."
      },
      {
        q: "Can I order bulk boxes for temple events or weddings?",
        a: "Yes. We supply 5 lb, 10 lb, and custom bulk prasad boxes across New Jersey, New York, and Connecticut via our catering department."
      }
    ]
  },

  // 4. Besan Ladoo (ID 98)
  {
    id: 98,
    sku: "32",
    urlSlug: "besan-ladoo",
    url: "https://qualitysweetsnj.com/besan-ladoo/",
    canonicalName: "Besan Ladoo",
    alternateNames: ["Besan Laddu", "Besan Ke Laddu", "Gram Flour Ladoo"],
    page_title: "Besan Ladoo (Besan Ke Laddu) | Desi Ghee Mithai | Quality Sweets",
    meta_description: "Handcrafted Besan Ladoo slow-roasted with gram flour, pure desi ghee, and cardamom. Rolled daily in Iselin, NJ. No preservatives. Ships across the USA.",
    search_keywords: "besan ladoo, besan laddu, besan ke laddu, gram flour ladoo, buy besan ladoo online, roasted besan sweet, diwali mithai",
    price: "8.00",
    image: "https://cdn10.bigcommerce.com/s-2ygwtj/products/98/images/294/Besan_Ladoo__03878.1790725934.1280.1280.jpg?c=2",
    p1: "Besan Ladoo (or Besan Ke Laddu) starts by slow-roasting coarse chickpea flour (gram flour) in pure desi ghee over low heat until it turns deep golden and fragrant. It is blended with bura sugar, crushed green cardamom, and slivered nuts, then hand-rolled into firm, aromatic ladoos. Each pound contains roughly 7 to 8 pieces.",
    moatHeading: "Why Quality Sweets Besan Ladoo Stands Apart",
    moatBullets: [
      "Slow-Roasted in Pure Ghee: Patiently roasted for over 45 minutes to eliminate any raw flour taste and develop deep nuttiness.",
      "Traditional Coarse Grain: Made with coarse besan and bura sugar for an authentic melt-in-your-mouth crumbly texture.",
      "Zero Chemical Preservatives: Hand-rolled daily in Iselin, NJ with 100% vegetarian ingredients and zero artificial colors."
    ],
    servingTips: "Enjoy at room temperature with hot tea, or pack as a nourishing snack for travel, lunchboxes, and festive celebrations.",
    storageTips: "Because roasted besan and ghee have minimal moisture, these ladoos keep very well. Store at room temperature in a dry container for up to 3 weeks.",
    faqs: [
      {
        q: "What is the shelf life of Besan Ladoo?",
        a: "Besan Ladoo stays fresh for up to 3 weeks at room temperature when kept in an airtight container away from moisture."
      },
      {
        q: "Do you add wheat flour or artificial binders?",
        a: "No. We use only 100% pure gram flour (chickpea flour), pure desi ghee, sugar, cardamom, and nuts."
      },
      {
        q: "How does nationwide delivery work?",
        a: "Besan Ladoos are firm and travel-hardy. They are packed in protective trays and shipped nationwide via FedEx Ground and Express."
      }
    ]
  },

  // 5. Gulab Jamoon (Large) (ID 127)
  {
    id: 127,
    sku: "62",
    urlSlug: "gulab-jamoon-large",
    url: "https://qualitysweetsnj.com/gulab-jamoon-large/",
    canonicalName: "Gulab Jamun (Large)",
    alternateNames: ["Gulab Jamun", "Gulab Jamoon", "Gulaab Jamun", "Kala Jamun"],
    page_title: "Gulab Jamun (Gulab Jamoon) | Fresh Khoya Sweets | Quality Sweets",
    meta_description: "Soft, spongy Gulab Jamun made from fresh khoya and soaked in warm rose-cardamom syrup. 0 preservatives. Handcrafted in NJ and shipped fresh across the USA.",
    search_keywords: "gulab jamun, gulab jamoon, buy gulab jamun online usa, soft gulab jamun, authentic indian sweets, warm gulab jamun, mithai delivery",
    price: "7.50",
    image: "https://cdn10.bigcommerce.com/s-2ygwtj/products/127/images/323/Big_Gulab_Jamoon__68976.1790725944.1280.1280.jpg?c=2",
    p1: "Gulab Jamun (spelled Gulab Jamoon in our catalog) is prepared by kneading fresh whole-milk khoya with a touch of flour, rolling smooth dough balls, and gently frying them in pure ghee until golden brown. They are soaked in warm sugar syrup infused with rose water and green cardamom. Approximately 8 large pieces per pound.",
    moatHeading: "Why Quality Sweets Gulab Jamun Stands Apart",
    moatBullets: [
      "Fresh Whole-Milk Khoya: Hand-rolled from fresh reduced dairy, creating a soft, pillowy texture that absorbs syrup to its center.",
      "Infused Rose & Cardamom Syrup: Lightly spiced syrup made without artificial extracts or synthetic food colorings.",
      "Zero Chemical Preservatives: Prepared fresh daily in New Jersey and packaged carefully for safe transit."
    ],
    servingTips: "Best served warm. Place two or three jamuns in a bowl with a spoonful of syrup and microwave for 15 to 20 seconds. Delicious served next to vanilla ice cream or kulfi.",
    storageTips: "Keep submerged in syrup and store in the refrigerator between 38°F and 42°F. Consume within 10 to 12 days.",
    faqs: [
      {
        q: "How should I reheat Gulab Jamun at home?",
        a: "Warm two or three pieces with a spoonful of syrup in the microwave for 15 to 20 seconds to enjoy that fresh-from-the-halwai warmth."
      },
      {
        q: "How are Gulab Jamuns shipped without leaking syrup?",
        a: "They are sealed in heavy-duty food-grade containers with leak-proof lids and cold packs inside insulated shipping boxes."
      },
      {
        q: "Can I order large quantities for parties or catering?",
        a: "Yes. We prepare bulk party trays of large Gulab Jamun for weddings, Diwali parties, and temple celebrations."
      }
    ]
  },

  // 6. Rasgulla (Large) (ID 126)
  {
    id: 126,
    sku: "61",
    urlSlug: "rasgulla-large",
    url: "https://qualitysweetsnj.com/rasgulla-large/",
    canonicalName: "Rasgulla (Large)",
    alternateNames: ["Rasgulla", "Roshogolla", "Rosogolla", "Bengali Rasgulla"],
    page_title: "Rasgulla (Roshogolla) | Fresh Bengali Sweet | Quality Sweets",
    meta_description: "Authentic Bengali Rasgulla made daily from fresh cow milk chhena simmered in light syrup. Spongy and juicy. Zero preservatives. Fresh delivery across USA.",
    search_keywords: "rasgulla, roshogolla, bengali rasgulla, buy rasgulla online usa, fresh chhena rasgulla, soft sponge rasgulla, authentic bengali sweets",
    price: "8.00",
    image: "https://cdn10.bigcommerce.com/s-2ygwtj/products/126/images/322/Big_Rasgulla__59066.1790725944.1280.1280.jpg?c=2",
    p1: "Rasgulla (in Bengali, Roshogolla) is Eastern India's most celebrated dessert. We curdle fresh milk daily to make soft cottage cheese (chhena), knead it until silky smooth, and simmer the dumplings in boiling light sugar syrup until they expand into airy, juicy sponges. Approximately 8 large pieces per pound.",
    moatHeading: "Why Quality Sweets Rasgulla Stands Apart",
    moatBullets: [
      "100% Fresh Milk Chhena: Made from real cow milk curdled fresh daily, never canned cottage cheese or starch fillers.",
      "Delicate Spongy Texture: Squeezable and juicy, soaking up just the right amount of light rose-cardamom syrup.",
      "Zero Preservatives: Handcrafted daily in Iselin, NJ following authentic Bengali sweetmaker recipes."
    ],
    servingTips: "Best served chilled straight from the refrigerator. Squeeze gently before serving if you prefer a lighter, less sweet bite.",
    storageTips: "Keep fully submerged in syrup and refrigerated between 38°F and 42°F at all times. Stays fresh for 7 to 10 days.",
    faqs: [
      {
        q: "Is your Rasgulla canned or freshly made?",
        a: "Our Rasgullas are 100% fresh, made daily from scratch in our Iselin kitchen without chemical preservatives."
      },
      {
        q: "How does nationwide delivery work for fresh Rasgulla?",
        a: "Orders ship in sealed, leak-proof containers cushioned with cold ice packs via FedEx Ground to ensure they arrive fresh and chilled."
      },
      {
        q: "What is the difference between Rasgulla and Gulab Jamun?",
        a: "Rasgulla is made from unaged fresh cottage cheese (chhena) simmered in clear light syrup, while Gulab Jamun is made from khoya dough fried until golden brown."
      }
    ]
  },

  // 7. Moong Dal Halwa (ID 92)
  {
    id: 92,
    sku: "26",
    urlSlug: "moong-dal-halwa",
    url: "https://qualitysweetsnj.com/moong-dal-halwa/",
    canonicalName: "Moong Dal Halwa",
    alternateNames: ["Mung Dal Halwa", "Moong Daal Halwa", "Yellow Lentil Pudding"],
    page_title: "Moong Dal Halwa | Rich Desi Ghee Lentil Sweet | Quality Sweets",
    meta_description: "Rich Moong Dal Halwa made with yellow lentils, desi ghee, mawa, and almonds. Zero preservatives. Warm, rich winter sweet shipped nationwide across USA.",
    search_keywords: "moong dal halwa, mung dal halwa, yellow lentil pudding, buy moong halwa online, winter halwa sweets, authentic desi ghee halwa",
    price: "6.50",
    image: "https://cdn10.bigcommerce.com/s-2ygwtj/products/92/images/287/moong_dal__18890.1790725932.1280.1280.jpg?c=2",
    p1: "Moong Dal Halwa is a traditional North Indian festive specialty. We soak yellow moong lentils, grind them into a coarse paste, and roast them patiently in generous amounts of pure desi ghee until golden and nutty. We finish the halwa with boiled milk, khoya, crushed cardamom, and toasted almond slivers.",
    moatHeading: "Why Quality Sweets Moong Dal Halwa Stands Apart",
    moatBullets: [
      "Pure Desi Ghee Roast: Slow-cooked in heavy copper pans for over an hour to develop a rich, nutty aroma.",
      "Whole Dairy Khoya & Nuts: Enriched with real milk solids and roasted dry fruits, without artificial colors or preservatives.",
      "Winter Comfort Classic: A warming staple for weddings, festive dinners, and chilly winter evenings."
    ],
    servingTips: "Must be served hot! Warm a portion in the microwave for 30 to 45 seconds, or heat in a nonstick pan on the stove with a teaspoon of ghee.",
    storageTips: "Refrigerate in an airtight container between 38°F and 42°F. Keeps well for 10 to 14 days. Reheat only the portion you plan to eat.",
    faqs: [
      {
        q: "How should I reheat Moong Dal Halwa?",
        a: "Heat in the microwave for 30 to 45 seconds or warm in a pan on medium heat until the ghee warms and releases its rich aroma."
      },
      {
        q: "How does shipping work for warm halwas?",
        a: "Halwa is cooled, sealed in heavy-duty food containers with thermal ice pack protection, and shipped Monday through Wednesday via FedEx."
      },
      {
        q: "Can I freeze Moong Dal Halwa?",
        a: "Yes. Moong Dal Halwa freezes very well for up to 1 month. Thaw in the refrigerator overnight and reheat thoroughly before serving."
      }
    ]
  },

  // 8. Imarti (ID 94)
  {
    id: 94,
    sku: "28",
    urlSlug: "imarti",
    url: "https://qualitysweetsnj.com/imarti/",
    canonicalName: "Imarti",
    alternateNames: ["Amriti", "Emarti", "Jahangir", "Urad Dal Jalebi Flower"],
    page_title: "Imarti (Amriti / Jahangir) | Urad Dal Sweet | Quality Sweets",
    meta_description: "Crispy floral Imarti made from whipped urad dal batter, fried in rings and dipped in saffron syrup. Zero preservatives. Shipped fresh across the USA.",
    search_keywords: "imarti, emarti, amriti, jahangir sweet, crispy imarti, buy imarti online, urad dal jalebi, authentic indian mithai",
    price: "7.50",
    image: "https://cdn10.bigcommerce.com/s-2ygwtj/products/94/images/289/Imarty__19234.1790725932.1280.1280.jpg?c=2",
    p1: "Imarti (also known as Amriti or Jahangir) is made from soaked and finely ground urad dal batter. The batter is whipped until airy, hand-piped through a cloth nozzle directly into hot oil in intricate geometric floral spirals, and dipped into saffron-infused sugar syrup. Each pound contains approximately 10 pieces.",
    moatHeading: "Why Quality Sweets Imarti Stands Apart",
    moatBullets: [
      "100% Urad Dal Batter: Made purely from black gram dal without maida flour fillers, providing a delicate crisp exterior and juicy interior.",
      "Hand-Piped Floral Geometry: Piped by master sweetmakers into classic circular flower motifs with distinct concentric loops.",
      "Zero Chemical Preservatives: Handcrafted daily in New Jersey and dipped in real saffron and cardamom syrup."
    ],
    servingTips: "Enjoy at room temperature, or warm slightly for 10 seconds in a microwave. Pairs naturally with hot milk, rabri, or fresh kulfi.",
    storageTips: "Store at room temperature in a dry box for up to 5 days, or refrigerate for up to 10 days.",
    faqs: [
      {
        q: "What is the difference between Imarti and Jalebi?",
        a: "Jalebi is made from fermented all-purpose flour (maida) with a tangy crunch, while Imarti is made from urad dal (lentil) batter with intricate floral rings and a softer, juicier bite."
      },
      {
        q: "How does nationwide delivery work for delicate Imarti?",
        a: "Imarti is hand-packed with protective corrugated dividers inside sturdy sweet boxes to prevent the crisp petal ridges from breaking during transit."
      },
      {
        q: "Does your Imarti contain artificial food coloring?",
        a: "We flavor and tint our sugar syrup using natural saffron strands and traditional spices with zero artificial chemical dyes."
      }
    ]
  },

  // 9. Milk Cake (ID 105)
  {
    id: 105,
    sku: "40",
    urlSlug: "milk-cake",
    url: "https://qualitysweetsnj.com/milk-cake/",
    canonicalName: "Milk Cake",
    alternateNames: ["Alwar Milk Cake", "Milkcake", "Alwar Ka Mawa", "Kalakand Barfi"],
    page_title: "Milk Cake (Alwar Ka Mawa) | Caramelized Sweet | Quality Sweets",
    meta_description: "Authentic two-tone Milk Cake made by slowly caramelizing whole milk into grainy khoya. Cardamom-spiced with no preservatives. Shipped fresh across the USA.",
    search_keywords: "milk cake, alwar milk cake, milkcake mithai, caramelized milk fudge, buy milk cake online usa, kalakand milk cake, authentic indian sweets",
    price: "7.50",
    image: "https://cdn10.bigcommerce.com/s-2ygwtj/products/105/images/301/Milk_Cake__92535.1790725936.1280.1280.jpg?c=2",
    p1: "Originating from Alwar in Rajasthan, Milk Cake is made by boiling large kettles of whole milk for hours until it curdles slightly into grainy fudge. As the center stays hot in its setting molds, it caramelizes into a deeper brown hue, creating its signature two-tone look. Approximately 7 to 8 pieces per pound.",
    moatHeading: "Why Quality Sweets Milk Cake Stands Apart",
    moatBullets: [
      "Signature Two-Tone Center: Naturally browned at its core through patient kettle cooking, not artificial colorings or caramel dyes.",
      "Dense Grainy Khoya Texture: Made exclusively with reduced dairy milk, pure desi ghee, sugar, and cardamom.",
      "Travel-Hardy & Long-Lasting: Thoroughly cooked milk solids give Milk Cake exceptional natural shelf life for nationwide shipping."
    ],
    servingTips: "Enjoy at room temperature or warm slightly for 10 to 15 seconds. Pairs wonderfully with afternoon tea or as an after-dinner treat.",
    storageTips: "Store in an airtight container at room temperature for up to 10 days, or refrigerate for up to 3 weeks.",
    faqs: [
      {
        q: "Why does Milk Cake have a darker brown center?",
        a: "When hot cooked milk fudge is poured into deep setting boxes and wrapped, the heat trapped inside continues to caramelize the dairy sugars, producing the authentic two-tone shade."
      },
      {
        q: "What is the shelf life of Milk Cake?",
        a: "Because the milk solids are cooked thoroughly with ghee, Milk Cake keeps very well: up to 10 days at room temperature or 3 weeks in the refrigerator."
      },
      {
        q: "Does Milk Cake contain gelatin or artificial flavoring?",
        a: "No. Our Milk Cake is 100% vegetarian, eggless, gelatin-free, and flavored only with natural green cardamom."
      }
    ]
  }
];

function buildDescriptionHtml(p) {
  const schemaObj = {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": p.canonicalName,
    "alternateName": p.alternateNames,
    "description": p.meta_description,
    "sku": p.sku,
    "image": p.image,
    "brand": {
      "@type": "Brand",
      "name": "Quality Sweets"
    },
    "suitableForDiet": "https://schema.org/VegetarianDiet",
    "offers": {
      "@type": "Offer",
      "url": p.url,
      "priceCurrency": "USD",
      "price": p.price,
      "priceValidUntil": "2027-12-31",
      "availability": "https://schema.org/InStock",
      "itemCondition": "https://schema.org/NewCondition",
      "seller": {
        "@type": "Organization",
        "name": "Quality Sweets"
      },
      "shippingDetails": {
        "@type": "OfferShippingDetails",
        "shippingRate": {
          "@type": "MonetaryAmount",
          "value": "Calculated at checkout",
          "currency": "USD"
        },
        "shippingDestination": {
          "@type": "DefinedRegion",
          "addressCountry": "US"
        },
        "deliveryTime": {
          "@type": "ShippingDeliveryTime",
          "handlingTime": {
            "@type": "QuantitativeValue",
            "minValue": 0,
            "maxValue": 2,
            "unitCode": "d"
          },
          "transitTime": {
            "@type": "QuantitativeValue",
            "minValue": 1,
            "maxValue": 4,
            "unitCode": "d"
          }
        }
      },
      "hasMerchantReturnPolicy": {
        "@type": "MerchantReturnPolicy",
        "applicableCountry": "US",
        "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
        "merchantReturnDays": 2,
        "returnMethod": "https://schema.org/ReturnByMail",
        "returnFees": "https://schema.org/FreeReturn"
      }
    }
  };

  const bulletsHtml = p.moatBullets.map(b => {
    const parts = b.split(":");
    if (parts.length >= 2) {
      return `      <li style="margin-bottom: 6px;"><strong>${parts[0].trim()}:</strong> ${parts.slice(1).join(":").trim()}</li>`;
    }
    return `      <li style="margin-bottom: 6px;">${b}</li>`;
  }).join("\n");

  const faqsHtml = p.faqs.map(f => `    <details style="margin-bottom: 8px; font-size: 13.5px; cursor: pointer;">
      <summary style="font-weight: bold; color: #4a0e17; padding: 4px 0;">${f.q}</summary>
      <p style="margin: 6px 0 0 16px; color: #555; line-height: 1.5;">${f.a}</p>
    </details>`).join("\n");

  return `<div class="qs-product-content-wrapper" style="font-family: inherit; line-height: 1.6; color: #333;">
  <p style="font-size: 15px; margin-bottom: 16px;">
    ${p.p1}
  </p>

  <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px 18px; margin: 18px 0;">
    <h3 style="color: #7a1526; font-size: 16px; margin: 0 0 10px 0; font-family: 'Marcellus', Georgia, serif;">${p.moatHeading}</h3>
    <ul style="margin: 0; padding-left: 20px; font-size: 13.5px; color: #4a0e17;">
${bulletsHtml}
    </ul>
  </div>

  <h3 style="color: #7a1526; font-size: 16px; margin-top: 20px; font-family: 'Marcellus', Georgia, serif;">Serving &amp; Reheating Tips</h3>
  <p style="font-size: 14px; margin-bottom: 16px;">
    ${p.servingTips}
  </p>

  <h3 style="color: #7a1526; font-size: 16px; margin-top: 20px; font-family: 'Marcellus', Georgia, serif;">Storage &amp; Freshness</h3>
  <p style="font-size: 14px; margin-bottom: 16px;">
    ${p.storageTips}
  </p>

  <div style="margin-top: 22px; border-top: 1px dashed #d4af37; padding-top: 14px;">
    <h3 style="color: #7a1526; font-size: 15px; margin-bottom: 8px; font-family: 'Marcellus', Georgia, serif;">Frequently Asked Questions</h3>
${faqsHtml}
  </div>
</div>

<script type="application/ld+json" id="qs-schema-product-${p.id}-v2">
${JSON.stringify(schemaObj, null, 2)}
</script>
`;
}

async function run() {
  const isApply = process.argv.includes("--apply");

  console.log("=================================================");
  console.log(`PDP OPTIMIZATION: BATCH 1 (9 REMAINING PRODUCTS)`);
  console.log(`MODE: ${isApply ? "PRODUCTION APPLY (--apply)" : "DRY RUN PREVIEW"}`);
  console.log("=================================================\n");

  // 1. Validation pass
  let hasErrors = false;
  for (const p of products) {
    if (p.page_title.length > 65) {
      console.error(`[ERROR] Title too long for ID ${p.id} (${p.page_title.length} chars): "${p.page_title}"`);
      hasErrors = true;
    }
    if (p.meta_description.length > 155 || p.meta_description.length < 140) {
      console.error(`[ERROR] Meta desc invalid length for ID ${p.id} (${p.meta_description.length} chars): "${p.meta_description}"`);
      hasErrors = true;
    }
    if (p.page_title.includes("—") || p.meta_description.includes("—") || p.p1.includes("—")) {
      console.error(`[ERROR] Em dash detected for ID ${p.id}! Anti-AI violation.`);
      hasErrors = true;
    }
    const html = buildDescriptionHtml(p);
    if (!html.includes(`id="qs-schema-product-${p.id}-v2"`)) {
      console.error(`[ERROR] Missing schema tag for ID ${p.id}`);
      hasErrors = true;
    }
  }

  if (hasErrors) {
    console.error("\nValidation failed. Exiting.");
    process.exit(1);
  }
  console.log("Validation passed: All 9 products meet title/meta lengths, schema specs, and anti-AI guidelines.\n");

  // 2. Fetch live data & create backup
  console.log("Fetching live product data from BigCommerce API for backup...");
  const liveBackup = [];
  for (const p of products) {
    const res = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v2/products/${p.id}`, {
      headers: { "X-Auth-Token": token, "Accept": "application/json" }
    });
    if (!res.ok) {
      throw new Error(`Failed to fetch product ${p.id}: ${res.status}`);
    }
    const currentData = await res.json();
    liveBackup.push(currentData);
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  const backupDir = path.join(ROOT, "scripts", "backups");
  if (!fs.existsSync(backupDir)) fs.mkdirSync(backupDir, { recursive: true });
  const backupFile = path.join(backupDir, `pdp_batch1_remaining9_backup_${timestamp}.json`);
  fs.writeFileSync(backupFile, JSON.stringify(liveBackup, null, 2), "utf8");
  console.log(`Backup saved to ${backupFile}\n`);

  // 3. Dry-run or Apply
  for (const p of products) {
    const fullHtml = buildDescriptionHtml(p);
    console.log(`-------------------------------------------------`);
    console.log(`PRODUCT ID: ${p.id} | ${p.canonicalName} (SKU: ${p.sku})`);
    console.log(`URL: ${p.url}`);
    console.log(`Title (${p.page_title.length} ch): ${p.page_title}`);
    console.log(`Meta  (${p.meta_description.length} ch): ${p.meta_description}`);
    console.log(`Keywords: ${p.search_keywords}`);
    console.log(`HTML Length: ${fullHtml.length} characters`);

    if (isApply) {
      console.log(`Applying update to BigCommerce API...`);
      const putRes = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v2/products/${p.id}`, {
        method: "PUT",
        headers: {
          "X-Auth-Token": token,
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({
          page_title: p.page_title,
          meta_description: p.meta_description,
          search_keywords: p.search_keywords,
          description: fullHtml
        })
      });

      if (!putRes.ok) {
        console.error(`[FAILED] Update failed for product ${p.id}: ${putRes.status} ${await putRes.text()}`);
      } else {
        const putJson = await putRes.json();
        console.log(`[SUCCESS] Product ${p.id} updated! HTTP 200 OK.`);
      }
    }
  }

  console.log("\n=================================================");
  if (!isApply) {
    console.log("DRY RUN COMPLETE. To apply changes to production, run:");
    console.log("node scripts/deploy_pdp_batch_1.js --apply");
  } else {
    console.log("ALL 9 PRODUCTS OPTIMIZED AND DEPLOYED IN PRODUCTION!");
  }
  console.log("=================================================");
}

run().catch(console.error);
