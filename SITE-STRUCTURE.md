# Arquitectura del Sitio y Jerarquía de URLs (BigCommerce)
**Proyecto:** Quality Sweets (`qualitysweetsnj.com`)  
**Modelo Operativo:** **Takeout & Pickup Only (No Dine-In)** en Tienda Física + Hub Regional Tri-State + E-commerce Nacional con Envíos a Todo USA  
**CMS:** BigCommerce  
**Sello Distintivo:** **100% Vegetarian | Made Fresh Daily in the USA | NO PRESERVATIVES**

---

## 1. Mapa General de Arquitectura de la Información

La **Homepage (`/`) es el Master Hub y Núcleo de Autoridad**. Concentra más del **80% del PageRank histórico** (desde 2003) y distribuye el flujo de enlaces (*link equity*) hacia los 5 pilares operativos:

```
                          ┌────────────────────────────────────────────────────────┐
                          │                      HOMEPAGE ( / )                    │
                          │   NÚCLEO CENTRAL & DISTRIBUIDOR DE AUTORIDAD (PILAR 0) │
                          │  - Posiciona términos de máxima competencia y marca     │
                          │  - Triaje de usuarios: Online / Takeout Local / B2B   │
                          │  - Distribuye PageRank e indexabilidad a los 5 pilares │
                          └───────────────────────────┬────────────────────────────┘
                                                      │
         ┌──────────────────┬─────────────────────────┼────────────────────────┬──────────────────────┐
         ▼                  ▼                         ▼                        ▼                      ▼
┌──────────────────┐ ┌────────────────────┐ ┌───────────────────┐ ┌───────────────────┐ ┌──────────────────────┐
│     PILAR 1      │ │      PILAR 2       │ │      PILAR 3      │ │      PILAR 4      │ │       PILAR 5        │
│  TAKEOUT & LOCAL │ │  TIENDA E-COMMERCE │ │     TRI-STATE     │ │   ESTACIONALES    │ │     AUTORIDAD &      │
│   PICKUP ISELIN  │ │   ENVÍOS USA       │ │  B2B & CATERING   │ │   FESTIVIDADES    │ │       E-E-A-T        │
│   (SIN DINE-IN)  │ │ (PRODUCTOS APTOS)  │ │   (NJ, NY, CT)    │ │  (URLS PERENNES)  │ │                      │
└────────┬─────────┘ └─────────┬──────────┘ └─────────┬─────────┘ └─────────┬─────────┘ └──────────┬───────────┘
         │                      │                      │                     │                      │
         ├─ /takeout-menu/      ├─ /indian-sweets/     ├─ /catering/         ├─ /seasonal/diwali    ├─ /about-us/
         ├─ /menu/chaats/       ├─ ↳ /bengali-sweets/  ├─ ↳ bodas y regalos  ├─ /seasonal/karwa     ├─ /in-the-media/
         ├─ /menu/street-food/  ├─ ↳ /barfi/           ├─ ↳ templos y prasad ├─ /seasonal/rakhi     ├─ /freshness-guarantee/
         ├─ /menu/mithai/       ├─ ↳ /traditional-mithai/  └─ ↳ samosas por volumen └─ /seasonal/holi ├─ /shipping-delivery/
         └─ /locations/iselin/  ├─ /indian-snacks/                                                 └─ /contact/ & WhatsApp
                                ├─ /mithai-box/
                                └─ /<product-slug>/...
```

---

## 2. Árbol Detallado de URLs por Pilar

```
qualitysweetsnj.com/
│
├── [/] (HOMEPAGE: MASTER HUB & TRIAGE HYBRID POWERHOUSE)
│   > Keyword exacta: "indian sweet shop" (8,100/mes | KD 23) + "indian sweet store" (8,100/mes) + "indian sweet shop near me" (8,100/mes)
│
├── [PILAR 1: EXPERIENCIA LOCAL ISELIN — TAKEOUT & PICKUP ONLY (NO DINE-IN)]
│   ├── /locations/iselin-nj/                 (Página local de tienda: mapa, horarios 10am-8pm, estacionamiento en Oak Tree Rd, takeout)
│   │                                         *Target: "indian sweets new jersey" (140/mes), "indian sweets edison nj" (110/mes), "iselin nj"*
│   ├── /menu/                                (Carta completa oficial de mostrador para llevar: Chaat, Street Food, Dulces y Bebidas)
│   │   ├── /menu/chaats/                     (Samosa Chaat, Kachori Chaat, Papri Chaat, Aloo Tikki Chaat, Pakoda Chaat)
│   │   ├── /menu/street-food-snacks/         (Pani Puri, Dahi Puri, Dahi Bhalla, Chole Bhatura, Chole Puri, Samosa casera, 
│   │   │                                      Paneer Pakoda, Cut Mirchy Pakoda, Dhokla, Aloo Tikki, Aloo Paratha, Ghobi Paratha)
│   │   ├── /menu/mithai-counter/             (Vitrina completa de dulces frescos por libra $/lb: 21 Bengalíes, 22 Tradicionales, 9 Burfis)
│   │   └── /menu/drinks/                     (Mango Lassi, Salt Lassi, Sweet Lassi, Masala Tea, Canned Soda, Water Bottles)
│   └── /live-jalebi-station/                 (Conexión de marca con Livejalebi.com para eventos y puestos en vivo)
│
├── [PILAR 2: E-COMMERCE NACIONAL — CATEGORÍAS EN RAÍZ "SEO OPTIMIZED (SHORT)" (BIGCOMMERCE)]
│   │   > Regla técnica: Solo productos empacados con protección térmica aptos para envíos de 1-2 días. El Chaat preparado NO se envía por paquetería.
│   │
│   ├── [CATEGORÍA MADRE DE DULCES — CATÁLOGO COMPLETO EN RAÍZ (52 VARIEDADES)]
│   │   └── /indian-sweets/                   [Keyword exacta: "indian sweets" — 18,100/mes | KD 33]
│   │                                         *Catálogo maestro de todos los dulces frescos con pastillas de filtro por subcategoría*
│   │
│   ├── [SUBCATEGORÍAS DE DULCES EN RAÍZ — URLS ULTRA LIMPIAS & BREADCRUMBS JERÁRQUICOS]
│   │   ├── /bengali-sweets/                  [Keyword exacta: "bengali sweets" — 2,900/mes] (Chum Chum en 5 sabores, Rasgulla, Sandesh, Kalakand — 21 variedades)
│   │   ├── /barfi/                           [Keyword exacta: "barfi" — 9,900/mes / "burfi" — 2,400/mes] (Kaju Katli puro [12,100/mes], Milk Cake, Pista Burfi — 9 variedades)
│   │   └── /traditional-mithai/              [Keyword exacta: "mithai" — 4,400/mes | KD 14] (Motichur Ladoo, Besan Ladoo, Kesar Peda, Gulab Jamun, Gujia, Jalebi — 22 variedades)
│   │
│   ├── [COLECCIONES HERMANAS INDEPENDIENTES EN RAÍZ]
│   │   ├── /indian-snacks/                   [Keyword exacta: "indian snacks" — 9,900/mes] (Mathi [1,000/mes], Namak Para [880/mes], Gud Para, Sev + Cashews especiadas — 11 variedades)
│   │   └── /mithai-box/                      [Keyword exacta: "mithai box" — 480/mes / "diwali sweets" — 2,900/mes] (Ganesh Boxes, Peacock Box, Baskets de 5 y 10 Lb, Karva Chauth Box — 28+ opciones)
│   │
│   └── [FICHAS DE PRODUCTO EN RAÍZ]
│       ├── /malai-chum-chum/
│       ├── /cherry-chum-chum/
│       ├── /gujia/
│       ├── /kesar-peda/
│       ├── /motichur-ladoo/
│       ├── /10-lb-assorted-sweets-gift-basket/
│       └── ... (Fichas de producto con selector de peso: 1 lb, 2 lb, 5 lb)
│
├── [PILAR 3: B2B, SERVICIOS & ALCANCE REGIONAL TRI-STATE (NJ, NY, CT)]
│   ├── /catering/                                      (Landing unificada de Catering & Pedidos por Volumen)
│   │   ├── #weddings-and-return-gifts                  (Mesas de dulces, return gift boxes y estaciones en vivo para bodas)
│   │   ├── #temple-and-mandir-prasad                   (Abastecimiento de Laddu, Peda y Prasad para Mandirs y Templos)
│   │   ├── #bulk-samosa-and-party-orders               (Bandejas de samosas, pakodas y chaat para eventos privados)
│   │   └── #corporate-gifting                          (Cajas personalizadas para empresas e instituciones)
│
├── [PILAR 4: ESTACIONALIDADES & FESTIVIDADES (LANDINGS PERENNES)]
│   ├── /seasonal/diwali-sweets-online/                 (URL permanente: Bengali Ladoo Basket, Peacock Gift Box, Ganesh Boxes)
│   ├── /seasonal/karva-chauth-specials/                (URL permanente: Karva Chauth Box, dulces tradicionales)
│   ├── /seasonal/raksha-bandhan-sweets/                (URL permanente: Cajas de regalo para hermanos con envío a todo USA)
│   └── /seasonal/holi-sweets-snacks/                   (URL permanente: Gujia tradicional, Namkeen, Thandai sweets)
│
└── [PILAR 5: AUTORIDAD, E-E-A-T & SERVICIO AL CLIENTE]
    ├── /about-us/                 (Historia desde 2003, tradición familiar de Sanjeev Saini, recetas sin conservantes hechas en EE. UU.)
    ├── /in-the-media/             (Apariciones en News 12 New Jersey, Revista Bon Appétit, reseñas de prensa)
    ├── /freshness-guarantee/      (Cómo empacamos, aislamiento térmico, garantía de frescura y política de 0 conservantes)
    ├── /shipping-delivery/        (Preguntas frecuentes de envíos nacionales, tiempos de tránsito, zonas de entrega express)
    ├── /reviews/                  (Testimonios verificados de clientes de mostrador y compradores online en todo EE. UU.)
    └── /contact/                  (Formulario directo, teléfono y mapa de cómo llegar a Iselin)
```

---

## 3. La Homepage (`/`): El Núcleo de Triaje y Autoridad

### ¿Por qué la Home es el Centro Neurálgico?
1. **Punto de Inyección de Autoridad:** Concentra la inmensa mayoría de los backlinks históricos (*News 12 NJ, Bon Appétit*, directorios locales de Edison/Iselin).
2. **Claridad Inmediata de Servicio:** Al entrar a la web, el usuario debe saber al instante:
   - **NO hay mesas para comer en el local** (evita malentendidos de comensales).
   - **SÍ hay mostrador para llevar (Takeout & Pickup)** con Chaat fresco, samosas calientes y dulces en Iselin, NJ.
   - **SÍ hay tienda online con envíos express a los 50 estados** de EE. UU.
   - **SÍ hay servicio B2B de bodas y templos** en todo el Tri-State (NJ, NY, CT).

### Wireframe Modular de la Homepage:

```
┌────────────────────────────────────────────────────────────────────────┐
│ [TOP BAR]: 🚚 Free Express Shipping on orders $60+ | NO PRESERVATIVES   │
│ [NAVBAR]: Logo | Shop Online (USA) | Takeout Menu (Iselin) | Catering | WhatsApp│
├────────────────────────────────────────────────────────────────────────┤
│ [HERO SECTION]:                                                        │
│   H1: Authentic Indian Sweet Shop — Handcrafted Mithai & Hot Snacks Daily│
│   Sub-H1: 100% Vegetarian, No Preservatives. Takeout & Pickup in Iselin│
│           or Shipped Fresh to Your Door Across the United States.      │
│                                                                        │
│   [TRIAGE DE 3 BOTONES PRINCIPALES (CTAs)]:                            │
│   ┌──────────────────────┐ ┌───────────────────┐ ┌───────────────────┐ │
│   │ 📦 Order Online      │ │ 🛍️ Takeout & Pickup│ │ 💍 Wedding/Temple │ │
│   │ (Nationwide Shipping)│ │ (Iselin Store Menu)│ │ (Tri-State Orders)│ │
│   └──────────────────────┘ └───────────────────┘ └───────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ [TRUST BADGES / E-E-A-T BAR]:                                          │
│   [★ Bon Appétit]  [★ News 12 NJ]  [NO PRESERVATIVES] [Since 2003]     │
├────────────────────────────────────────────────────────────────────────┤
│ [VITRINA E-COMMERCE: DULCES Y CAJAS DESTACADAS]:                       │
│   H2: Fresh Indian Mithai Shipped Across America                       │
│   - Chum Chum, Kaju Katli, Motichur Ladoo, Karva Chauth Box, Baskets   │
│   [Button: Shop All Sweets -> /indian-sweets/]                          │
├────────────────────────────────────────────────────────────────────────┤
│ [MOSTRADOR DE COMIDA CALIENTE & CHAAT (TAKEOUT ONLY)]:                 │
│   H2: Hot Samosas, Chaats & Street Food to Go                          │
│   *Nota destacada: Order ahead for pickup at 1384 Oak Tree Rd (No Dine-In)*│
│   - Pani Puri, Dahi Bhalla, Chole Bhatura, Samosas recién hechas       │
│   - Horarios: 7 días, 10:00 AM - 8:00 PM                               │
│   [Button: View Full Takeout Menu -> /menu/] [Button: Order via WhatsApp]│
├────────────────────────────────────────────────────────────────────────┤
│ [B2B & EVENTOS REGIONALES (NJ, NY, CT)]:                               │
│   H2: Authentic Mithai & Samosas for Weddings, Mandirs & Bulk Events   │
│   - Precios mayoristas para templos, bandejas de 50-1000+ samosas      │
│   [Button: Bulk & Catering Inquiries -> /catering/]                    │
├────────────────────────────────────────────────────────────────────────┤
│ [GARANTÍA DE CALIDAD Y FRESCURA]:                                      │
│   H2: The Quality Sweets Promise: Zero Preservatives, Pure Ingredients │
│   - Cómo mantenemos la frescura artesanal en empaques térmicos exprés   │
├────────────────────────────────────────────────────────────────────────┤
│ [PRUEBA SOCIAL]:                                                       │
│   H2: Over 20+ Years Serving the Tri-State & Sweet Lovers Nationwide   │
│   - Reseñas verificadas de Google y compradores online                 │
├────────────────────────────────────────────────────────────────────────┤
│ [FOOTER SEO ESTRUCTURADO]:                                             │
│   - Columna 1: Dirección oficial en Iselin, teléfono, WhatsApp y mapa  │
│   - Columna 2: Categorías de e-commerce (dulces, burfis, snacks, cajas)│
│   - Columna 3: Carta de Takeout & Recogida (Chaats, Samosas, Parathas) │
│   - Columna 4: Catering Tri-State, Prensa, Envíos y FAQ                │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Coexistencia Sin Fricción y Reglas de Envío (Fulfillment Matrix)

Confirmación oficial del modelo operativo: **NADA de la comida preparada ni bebidas del volante se envía por paquetería; TODO lo demás (dulces, burfis, snacks secos, nueces y cajas de regalo) SÍ se envía a todo EE. UU.**:

| Grupo de Productos | ¿Se Envía a Todo USA? | ¿Disponible para Takeout / Pickup? | URL / Destino en la Web | Regla Técnica en BigCommerce & Comportamiento UI |
|---|:---:|:---:|---|---|
| **Comida Caliente & Chaats**<br>*(Samosas, Pani Puri, Chole Bhatura, Parathas, Lassis)* | ❌ **NO** | ✅ **SÍ (Exclusivo)** | `/menu/` *(Chaats, Street food, Drinks)* | **Non-Shippable:** En el checkout solo permite *"In-Store Pickup / Takeout"*. La UI muestra botón *"Order for Pickup / WhatsApp"* con aviso: *"Prepared hot daily — Iselin pickup only"*. |
| **All Indian Sweets (Catálogo Madre)**<br>*(Vitrina completa de 52 variedades de dulces)* | ✅ **SÍ** *(Con empaque térmico)* | ✅ **SÍ** | `/indian-sweets/`<br>y vitrina de tienda | **Shippable & Pickup:** Vista de catálogo completa con selector de entrega y filtros por subcategoría. |
| **Dulces Bengalíes (Subcategoría 1)**<br>*(Chum Chum, Rasgulla, Sandesh, Kalakand)* | ✅ **SÍ** *(Con ice packs)* | ✅ **SÍ** | `/bengali-sweets/`<br>y vitrina de mostrador | **Shippable & Pickup:** La UI muestra el selector: `[ 🚚 Ship Nationwide ]` o `[ 🏪 Pick up in Iselin, NJ ]`. Empaque térmico con hielo seco. |
| **Barfi & Kaju Katli (Subcategoría 2)**<br>*(Kaju Katli puro, Milk Cake, Pista Burfi)* | ✅ **SÍ** | ✅ **SÍ** | `/barfi/`<br>y vitrina de mostrador | **Shippable & Pickup:** Alta resistencia al transporte de 2-3 días. Selector dual de entrega. |
| **Dulces Tradicionales (Subcategoría 3)**<br>*(Motichur Ladoo, Peda, Gulab Jamun, Jalebi, Gujia)* | ✅ **SÍ** | ✅ **SÍ** | `/traditional-mithai/`<br>y vitrina de mostrador | **Shippable & Pickup:** Selector dual en ficha de producto. Empaque hermético con fecha de elaboración. |
| **Snacks Secos Empacados (Hermana)**<br>*(Mathi, Gud Para, Sakar Para, Namak Para, Sev)* | ✅ **SÍ** | ✅ **SÍ** | `/indian-snacks/`<br>y estantes de tienda | **Shippable & Pickup:** Producto seco de larga vida útil sin refrigeración. Envíos económicos estándar o express. |
| **Cajas de Regalo y Festividades (Hermana)**<br>*(Diwali Baskets, Ganesh Boxes, Karva Chauth)* | ✅ **SÍ** | ✅ **SÍ** | `/mithai-box/`<br>y vitrina de temporada | **Shippable & Pickup:** Cajas de lujo listas para obsequiar a familiares o clientes en cualquier estado de EE. UU. |

---

## 5. Schema.org JSON-LD (Marcado Híbrido Validado)

### Marcado de la Homepage (`FoodEstablishment` + `OnlineStore`)
Configurado específicamente para **declarar servicio para llevar y envíos, excluyendo expresamente el servicio de mesas**:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://qualitysweetsnj.com/#website",
      "url": "https://qualitysweetsnj.com/",
      "name": "Quality Sweets - Indian Sweets Shop",
      "description": "Authentic Indian Sweets, Chaats & Snacks Handcrafted Daily with No Preservatives. Takeout & Pickup in Iselin, NJ & Nationwide Shipping Across the USA.",
      "publisher": {
        "@id": "https://qualitysweetsnj.com/#localbusiness"
      },
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://qualitysweetsnj.com/search.php?search_query={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    },
    {
      "@type": ["FoodEstablishment", "OnlineStore"],
      "@id": "https://qualitysweetsnj.com/#localbusiness",
      "name": "Quality Sweets - Indian Sweets Shop",
      "alternateName": ["Quality Sweets", "Quality Sweets NJ"],
      "image": "https://qualitysweetsnj.com/images/storefront-quality-sweets.jpg",
      "url": "https://qualitysweetsnj.com/",
      "telephone": "+1-732-283-3799",
      "priceRange": "$$",
      "acceptsReservations": false,
      "hasMenu": "https://qualitysweetsnj.com/menu/",
      "servesCuisine": ["Indian", "Bengali Sweets", "North Indian Snacks", "Vegetarian", "Chaat"],
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "1384 Oak Tree Road",
        "addressLocality": "Iselin",
        "addressRegion": "NJ",
        "postalCode": "08830",
        "addressCountry": "US"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 40.5695,
        "longitude": -74.3298
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
          "opens": "10:00",
          "closes": "20:00"
        }
      ],
      "sameAs": [
        "https://www.facebook.com/qualitysweetsnj",
        "https://www.instagram.com/qualitysweetsnj"
      ],
      "areaServed": [
        {"@type": "City", "name": "Iselin"},
        {"@type": "City", "name": "Edison"},
        {"@type": "City", "name": "Woodbridge"},
        {"@type": "City", "name": "New Brunswick"},
        {"@type": "State", "name": "New Jersey"},
        {"@type": "State", "name": "New York"},
        {"@type": "State", "name": "Connecticut"},
        {"@type": "Country", "name": "United States"}
      ]
    }
  ]
}
```

---

## 6. Estrategia de Enlazado Interno y Menú de Navegación (Header)

En el encabezado de BigCommerce, la navegación refleja con precisión la jerarquía gastronómica y comercial:

1. **Shop Online (USA Delivery)** ➔ Mega menú desplegable con la jerarquía Padre/Hijas:
   * **All Indian Sweets (`/indian-sweets/`)** [Catálogo Completo de 52 Dulces Frescos]
     * ↳ *Bengali Sweets (`/bengali-sweets/`) — Chum Chum, Rasgulla, Sandesh, Kalakand*
     * ↳ *Barfi & Kaju Katli (`/barfi/`) — Kaju Katli puro, Milk Cake, Pista Burfi*
     * ↳ *Traditional Mithai (`/traditional-mithai/`) — Motichur Ladoo, Kesar Peda, Gulab Jamun, Gujia, Jalebi*
   * **Indian Snacks & Namkeen (`/indian-snacks/`)** — Mathi, Gud Para, Namak Para, Sev & Cashews especiadas
   * **Mithai Boxes & Gift Baskets (`/mithai-box/`)** — Diwali Specials, Ganesh Boxes, Karva Chauth Box
2. **Takeout Menu (Iselin, NJ)** ➔ Desplegable con la carta física para llevar (No Dine-In):
   * *Chaats (Pani Puri, Dahi Bhalla, Samosa Chaat, Papri Chaat)*
   * *Hot Street Food (Chole Bhatura, Samosas del día, Pakodas, Parathas)*
   * *Mithai Counter by the Pound ($/lb)*
   * *Drinks (Mango Lassi, Sweet Lassi, Masala Tea)*
3. **Catering & Bulk Orders (Tri-State) (`/catering/`)** ➔ Una única landing con soluciones para bodas, templos, regalos corporativos y fiestas familiares en NJ, NY y CT.
4. **Store Location & Hours (`/locations/iselin-nj/`)** ➔ Landing local de Iselin con horarios, mapa de estacionamiento en Oak Tree Rd y cómo llegar desde NYC/CT.
5. **About Us & Press** ➔ Más de 20 años de historia, News 12 NJ, Bon Appétit y compromiso de cero conservantes.
6. **Llamar a la tienda** ➔ Acción rápida para pedidos de mostrador y consultas mayoristas.

---

## 7. Decisión Técnica de Taxonomía y URLs: "SEO Optimized (Short)" en Raíz (Estándar BigCommerce 2026)

Se adopta formalmente la arquitectura de **URLs en Raíz sin prefijo `/collections/`**, utilizando la funcionalidad nativa de BigCommerce **"SEO Optimized (Short)"** (*Settings > Store Setup > URL Structure*):

### 1. Eliminación del Prefijo Legado `/collections/`:
* El prefijo `/collections/` es una limitación histórica del enrutamiento de Shopify. En BigCommerce no aporta ningún valor y alarga artificialmente las URLs.
* En 2026, los motores de búsqueda y los agentes de búsqueda de IA (Perplexity, ChatGPT, Google AI Overviews) premian la concisión, la relevancia directa de raíz y las URLs semánticas limpias.

### 2. Relación de Catálogo (Padre / Hijas en Raíz):
* **Colección Paraguas (Madre):** `/indian-sweets/` alberga los **52 dulces** de la tienda. Incluye filtros visuales en la cabecera: `[ Ver Todos (52) ]` `[ Bengali Sweets (21) ]` `[ Barfi & Kaju (9) ]` `[ Traditional Mithai (22) ]`. Ataca la keyword de mayor volumen del sector: **`indian sweets`** (18,100 búsquedas/mes | KD 33).
* **Subcategorías Especializadas en Raíz (Hijas):**
  * `/bengali-sweets/` ➔ Ataca **`bengali sweets`** (2,900/mes).
  * `/barfi/` ➔ Ataca **`barfi`** (9,900/mes) y **`kaju katli`** (12,100/mes).
  * `/traditional-mithai/` ➔ Ataca **`mithai`** (4,400/mes).
* **Colecciones Hermanas en Raíz:**
  * `/indian-snacks/` ➔ Ataca **`indian snacks`** (9,900/mes).
  * `/mithai-box/` ➔ Ataca **`mithai box`** (480/mes) y **`diwali sweets`** (2,900/mes).

### 3. Fichas de Producto (Aislamiento de Slugs):
* Los productos usan URLs cortas en la raíz: `/<nombre-del-producto>/` (ej.: `/malai-chum-chum/`).
* Esto garantiza **cero conflictos de slugs** entre productos y categorías en BigCommerce.

### 4. Migas de Pan Estructuradas (Breadcrumbs Schema):
Aunque las URLs vivan en la raíz, la jerarquía visual y de datos estructurados para Google se mantiene íntegra a través de `BreadcrumbList`:
* `Home` ➔ `Indian Sweets` ➔ `Bengali Sweets` ➔ `Malai Chum Chum`
* `Home` ➔ `Indian Sweets` ➔ `Barfi & Kaju` ➔ `Pure Kaju Katli`
* `Home` ➔ `Indian Sweets` ➔ `Traditional Mithai` ➔ `Motichur Ladoo Box`
* `Home` ➔ `Indian Snacks` ➔ `Traditional Mathi`
* `Home` ➔ `Mithai Boxes` ➔ `Golden Ganesh Box`

### 5. Protocolo de Redirecciones 301 en Migración:
Al activar *"SEO Optimized (Short)"* en BigCommerce:
* Asegurar que cualquier URL previa que contuviera `/collections/` o `/categories/` tenga su correspondiente regla de redirección 301 permanente en *Server Settings > 301 Redirects*.
* Validar que el sitemap XML se regenere automáticamente con las nuevas URLs en raíz.
