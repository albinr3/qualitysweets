# Guía Oficial de Estructura y Nomenclatura de UTMs (Quality Sweets)

**Sitio web:** `https://qualitysweetsnj.com`  
**Objetivo:** Estandarizar el etiquetado de enlaces externos para atribuir con total precisión el tráfico y las conversiones en Google Analytics 4 (GA4) provenientes de Google Business Profile (GBP), empaques físicos (códigos QR), difusión en WhatsApp, redes sociales y campañas directas.

---

## 1. Principios y Reglas Universales de Etiquetado

1. **Minúsculas estrictas (`lowercase`):**  
   GA4 distingue entre mayúsculas y minúsculas (`Organic` $\neq$ `organic`). Todos los parámetros deben escribirse en minúsculas.
2. **Separadores consistentes:**  
   Utilizar guion bajo (`_`) para separar palabras dentro de los valores de parámetros (ej. `google_business_profile`, `gbp_diwali`).
3. **Prohibido el uso de UTMs en enlaces internos:**  
   **Nunca** colocar parámetros UTM en enlaces internos de la propia web (`qualitysweetsnj.com`). Esto destruiría la sesión de usuario en GA4 y sobreescribiría la fuente de atribución real.
4. **Respeto a las URLs canónicas:**  
   Las URLs con UTMs deben mantener la barra diagonal final (`/`) antes del signo `?` para evitar redirecciones 301 innecesarias de BigCommerce que puedan perder parámetros:
   * *Correcto:* `https://qualitysweetsnj.com/menu/?utm_source=...`
   * *Incorrecto:* `https://qualitysweetsnj.com/menu?utm_source=...` (provoca redirección 301 a `/menu/`).
5. **No incluir datos personales (PII):**  
   Nunca incluir nombres, correos o números de teléfono en los parámetros UTM.

---

## 2. Parámetros Estándar

| Parámetro | Obligatorio | Descripción y Función | Ejemplo |
|---|---|---|---|
| `utm_source` | **Sí** | Plataforma o herramienta que origina el clic. | `google_business_profile`, `whatsapp`, `packaging_qr` |
| `utm_medium` | **Sí** | Medio o canal de distribución del tráfico. | `organic`, `offline`, `social_messaging` |
| `utm_campaign` | **Sí** | Nombre específico de la iniciativa, festival o campaña. | `gbp_local`, `gbp_diwali`, `sweet_box_insert` |
| `utm_content` | Opcional | Elemento específico sobre el que se hizo clic o variante. | `website_button`, `menu_button`, `reorder_sweets` |
| `utm_term` | Opcional | Keyword asociada (usado principalmente en Paid Search). | N/A para tráfico orgánico. |

---

## 3. Estructura por Canal de Marketing

### 3.1. Google Business Profile (Ficha Principal en Google Maps / Local Pack)

Permite separar el tráfico orgánico puro del sitio web del tráfico derivado directamente de la ficha local en Google Maps.

* **Botón principal "Sitio web" (Website Button):**
  * **Destino:** Página local de Iselin (`/locations/iselin-nj/`) o Homepage (`/`).
  * **URL:**  
    `https://qualitysweetsnj.com/locations/iselin-nj/?utm_source=google_business_profile&utm_medium=organic&utm_campaign=gbp_listing&utm_content=website_button`

* **Botón de pedidos / menú (Menu Button):**
  * **Destino:** `/menu/`
  * **URL:**  
    `https://qualitysweetsnj.com/menu/?utm_source=google_business_profile&utm_medium=organic&utm_campaign=gbp_listing&utm_content=menu_button`

---

### 3.2. Publicaciones Semanales de Google Business Profile (52 Semanas)

Estructura ya implementada en el calendario anual (`Calendario_GBP_52_Semanas_Quality_Sweets.xlsx`).

* **Estructura base:**  
  `https://qualitysweetsnj.com{path}/?utm_source=google_business_profile&utm_medium=organic&utm_campaign=gbp_{slug}`

* **Matriz de campañas por categoría y estacionalidad:**
  * **Página local / General:** `utm_campaign=gbp_local`
  * **Dulces Bengalíes:** `utm_campaign=gbp_bengali`
  * **Barfi & Kaju Katli:** `utm_campaign=gbp_barfi` o `gbp_kaju_katli`
  * **Mithai Tradicional & Ladoos:** `utm_campaign=gbp_mithai` o `gbp_ladoo`
  * **Snacks & Namkeen:** `utm_campaign=gbp_snacks`
  * **Comida para Llevar & Chaat:** `utm_campaign=gbp_chaat`, `gbp_samosa`, `gbp_pani_puri`
  * **Catering & Eventos:** `utm_campaign=gbp_weddings`, `gbp_catering`, `gbp_samosa_catering`
  * **Festivales Clave:**
    * Diwali anticipado: `utm_campaign=gbp_diwali_early`
    * Semana Diwali: `utm_campaign=gbp_diwali`
    * Post-Diwali: `utm_campaign=gbp_post_diwali`
    * Holi anticipado: `utm_campaign=gbp_holi_early`
    * Semana Holi: `utm_campaign=gbp_holi_week`
    * Raksha Bandhan: `utm_campaign=gbp_rakhi`

---

### 3.3. Empaques Físicos e Insertos (Offline-to-Online QR Codes)

Medición de clientes que ya compran en tienda y escanean el código QR en las cajas de dulces para volver a pedir online o consultar menús.

* **Reorden de cajas de dulces (Insertos en cajas de 1 lb / 2 lb / Cestas):**
  * **Destino:** `/mithai-box/` o `/indian-sweets/`
  * **URL:**  
    `https://qualitysweetsnj.com/mithai-box/?utm_source=packaging_qr&utm_medium=offline&utm_campaign=sweet_box_insert&utm_content=reorder_sweets`

* **QR en empaques de comida para llevar (Bolsas de Takeout / Chaat):**
  * **Destino:** `/menu/`
  * **URL:**  
    `https://qualitysweetsnj.com/menu/?utm_source=packaging_qr&utm_medium=offline&utm_campaign=takeout_bag_insert&utm_content=view_menu`

* **Cajas de bodas y eventos especiales (Muestrarios de Catering):**
  * **Destino:** `/catering/`
  * **URL:**  
    `https://qualitysweetsnj.com/catering/?utm_source=packaging_qr&utm_medium=offline&utm_campaign=wedding_box_sample&utm_content=catering_quote`

---

### 3.4. WhatsApp y Mensajería Directa (Pedidos de Mostrador y Avisos)

* **Lista de difusión de especiales de fin de semana (Takeout):**
  * **Destino:** `/menu/`
  * **URL:**  
    `https://qualitysweetsnj.com/menu/?utm_source=whatsapp&utm_medium=social_messaging&utm_campaign=weekend_takeout&utm_content=specials_broadcast`

* **Preventa de cajas festivas (Diwali, Karwa Chauth, Holi):**
  * **Destino:** `/mithai-box/`
  * **URL:**  
    `https://qualitysweetsnj.com/mithai-box/?utm_source=whatsapp&utm_medium=social_messaging&utm_campaign=festival_preorder&utm_content=whatsapp_broadcast`

---

### 3.5. Redes Sociales Orgánicas (Instagram, Facebook, TikTok)

* **Enlace de la biografía (Link in Bio / Árbol de enlaces):**
  * Menú Takeout: `https://qualitysweetsnj.com/menu/?utm_source=instagram&utm_medium=social&utm_campaign=bio_link&utm_content=menu_button`
  * Tienda Online de Dulces: `https://qualitysweetsnj.com/indian-sweets/?utm_source=instagram&utm_medium=social&utm_campaign=bio_link&utm_content=shop_sweets`
  * Formulario de Catering: `https://qualitysweetsnj.com/catering/?utm_source=instagram&utm_medium=social&utm_campaign=bio_link&utm_content=catering_button`

* **Publicaciones en historias o posts promocionales:**
  * `https://qualitysweetsnj.com/bengali-sweets/?utm_source=facebook&utm_medium=social&utm_campaign=bengali_sweets_launch&utm_content=post_chum_chum`

---

## 4. Matriz Rápida de Atribución (Cheat Sheet)

| Canal / Acción | `utm_source` | `utm_medium` | `utm_campaign` | `utm_content` | Página de Destino Recomendada |
|---|---|---|---|---|---|
| **GBP Ficha: Sitio Web** | `google_business_profile` | `organic` | `gbp_listing` | `website_button` | `/locations/iselin-nj/` |
| **GBP Ficha: Menú** | `google_business_profile` | `organic` | `gbp_listing` | `menu_button` | `/menu/` |
| **GBP Post Semanal** | `google_business_profile` | `organic` | `gbp_{slug}` | *(vacío)* | Variable según publicación |
| **QR Caja de Dulces** | `packaging_qr` | `offline` | `sweet_box_insert` | `reorder_sweets` | `/mithai-box/` |
| **QR Bolsa Takeout** | `packaging_qr` | `offline` | `takeout_bag_insert` | `view_menu` | `/menu/` |
| **WhatsApp Especiales** | `whatsapp` | `social_messaging` | `weekend_takeout` | `specials_broadcast` | `/menu/` |
| **WhatsApp Festivo** | `whatsapp` | `social_messaging` | `festival_preorder` | `whatsapp_broadcast` | `/mithai-box/` |
| **Instagram Bio (Menú)**| `instagram` | `social` | `bio_link` | `menu_button` | `/menu/` |
| **Instagram Bio (Dulces)**| `instagram` | `social` | `bio_link` | `shop_sweets` | `/indian-sweets/` |

---

## 5. Visualización y Validación en Google Analytics 4

1. **Pruebas en tiempo real:**
   * Abrir la URL generada en una ventana de incógnito.
   * Ir a **GA4 > Administración > DebugView** o **Informes > En tiempo real**.
   * Verificar que el evento `session_start` y `page_view` contengan los parámetros:
     * `source` / `session_source`: según el valor de `utm_source`.
     * `medium` / `session_medium`: según el valor de `utm_medium`.
     * `campaign` / `session_campaign`: según el valor de `utm_campaign`.
2. **Cruce con Eventos de Conversión:**
   * Al estar configurados los eventos clave del sitio ([deploy_ga4_native_3_2.js](file:///c:/Users/Albin%20Rodriguez/Documents/QualitySweets/scripts/deploy_ga4_native_3_2.js)), en los informes de exploración se podrá filtrar qué campañas de GBP, QR o WhatsApp generaron:
     * `click_call_store` (Llamadas telefónicas)
     * `click_directions` (Solicitud de ruta en Google Maps)
     * `view_takeout_menu` (Visualizaciones del menú para llevar)
     * `catering_quote_start` (Inicios de cotización para eventos)
     * `purchase` (Compras completadas en el e-commerce)
