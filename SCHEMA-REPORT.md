# Auditoría de Schema — Quality Sweets

**Actualizada:** 2026-09-16  
**Alcance:** HTML fuente publicado en `qualitysweetsnj.com`, Catalog API de BigCommerce y despliegue Blueprint administrado por API.

## URLs retiradas

Estas rutas no son páginas activas, no reciben marcado propio y no deben usarse en enlaces internos:

| URL retirada | HTTP | Destino confirmado |
|---|---:|---|
| `/catering/wedding-catering-tri-state/` | 301 | `/catering/` |
| `/catering/temple-mandir-bulk-prasad/` | 301 | `/catering/` |
| `/catering/bulk-samosa-orders/` | 301 | `/catering/` |

Los contenidos de bodas, templos y samosas viven como secciones de la landing activa `/catering/`.

## Marcado publicado y comprobado

| URL / cobertura | JSON-LD | Resultado en HTML fuente |
|---|---|---|
| `/` | `WebSite` + `FoodEstablishment` + `OnlineStore` | Publicado como un grafo con entidad principal `https://qualitysweetsnj.com/#business`. |
| `/catering/` | `CateringService` | Publicado; `provider.@id` apunta a `#business`. |
| 9 categorías comerciales visibles | `CollectionPage` + `BreadcrumbList` | Publicado mediante la descripción de categoría. `Takeout Menu` y `Catering` quedan excluidas por intención. |
| 88 PDP visibles | `Product` | Publicado desde Catalog API. Solo lleva `ProductGroup` si BigCommerce entrega variantes reales. |
| PDP enviable, p. ej. `/bengali-ladoo-basket-diwali-special/` | `Product` + `Offer` | Precio, URL, imagen, SKU y disponibilidad proceden del catálogo. El ejemplo publicado declara `InStock` y precio `125`. |
| PDP pickup-only, p. ej. `/malai-chum-chum/` | `Product` sin `Offer` | No declara precio, envío ni compra web. |
| `/contact-us/` | `ContactPage` | Publicado y vinculado a `#business`. |
| `/locations/iselin-nj/` | `WebPage` | Publicado con referencia a la única entidad física `#business`; no crea otro `LocalBusiness`. |

La entidad de homepage usa los datos publicados y verificados: 1384 Oak Tree Road, Iselin, NJ 08830; `+17322833799`; horario diario 10:00–20:00; coordenadas `40.5739404,-74.3261661`; menú y redes sociales actuales.

## Reglas aplicadas

- `FoodEstablishment` ya hereda de `LocalBusiness`; no se publica un `LocalBusiness` duplicado.
- Los modificadores de peso se modelan como `Product`, no como variantes. `ProductGroup` queda condicionado a variantes reales con datos propios de catálogo.
- Un `Offer` solo se añade a productos cuya disponibilidad de BigCommerce es `available` y cuyo precio publicado es real.
- No se publica `shippingDetails` ni devolución: las reglas de checkout/envíos no se inventan.
- No se publica `FAQPage`, `AggregateRating` ni reseñas.
- El menú se referencia con `hasMenu` desde la entidad principal; no existe una entidad `Menu` que requiera sincronización de platos.

## Validación realizada

- Todos los bloques JSON-LD comprobados parsean como JSON y aparecen en el código fuente HTTP, sin depender de JavaScript en el navegador.
- Se verificaron fuente y tipos en homepage, `/catering/`, una categoría, un PDP enviable, un PDP pickup-only, contacto y ubicación.
- Los precios, SKU, disponibilidad y URL de los PDP comprobados coinciden con Catalog API.
- Las tres URLs antiguas responden 301 a `/catering/` y no contienen marcado propio.
- El despliegue se ejecutó primero en modo dry-run y, tras publicar en lotes, cada lote vuelve a dry-run con cero cambios: el proceso es idempotente.

La comprobación en Schema.org Validator y Google Rich Results Test sigue siendo una verificación manual externa recomendada para las cuatro URLs representativas, ya que esas interfaces no ofrecen una API de validación automatizable en este repositorio.

## Artefactos de implementación

- `scripts/deploy_schema_blueprint_3_1.js`: despliegue idempotente con dry-run por defecto y respaldos antes de escribir.
- `scripts/backups/schema-blueprint-before-*.json`: estado previo recuperable de los recursos modificados.
- `IMPLEMENTATION-ROADMAP.md`: Fase 3 corregida para BigCommerce Legacy Blueprint.
