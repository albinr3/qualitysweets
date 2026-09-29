# Auditoría y Validación Técnica del Sitemap XML
**Sitio Web:** [qualitysweetsnj.com](https://qualitysweetsnj.com)  
**Plataforma:** BigCommerce (Blueprint)  
**Fecha de Análisis y Corrección:** 21 de Septiembre de 2026  
**URL Oficial del Sitemap Index:** `https://qualitysweetsnj.com/xmlsitemap.php`  
**Estado General:** ✅ **100% Saludable (0 Errores, 0 Redirecciones, 113/113 URLs en HTTP 200 OK)**

---

## 1. Diagnóstico: ¿Por qué Google Search Console reportó problemas?

Al auditar la configuración del servidor, los archivos en vivo y el comportamiento de BigCommerce, se identificaron **dos causas directas** por las cuales Google Search Console marcó errores o advertencias:

### Causa 1: Envío de `sitemap.xml` en lugar de `xmlsitemap.php` (Error Crítico 404)
* **El Problema:** Por costumbre, en Google Search Console casi todo el mundo escribe `sitemap.xml`. Sin embargo, en BigCommerce el archivo nativo se llama **`xmlsitemap.php`**. 
* **Qué veía Googlebot:** Al solicitar `https://qualitysweetsnj.com/sitemap.xml`, el servidor devolvía un código de estado **`HTTP 404 Not Found`** con una página HTML completa (*"Quality Sweets - Not Found"*).
* **Mensaje de Google Search Console:** 
  > *"No se ha podido recuperar"* (*Couldn't fetch*) o *"El sitemap parece ser una página HTML"* (*Sitemap is an HTML page*).

### Causa 2: URL con Redirección 301 dentro del Sitemap de Categorías (Error de Calidad)
* **El Problema:** Dentro del sub-sitemap de categorías (`xmlsitemap.php?type=categories&page=1`), aparecía la URL:
  ```xml
  <loc>https://qualitysweetsnj.com/chaats/</loc>
  ```
* **Qué ocurría:** La categoría 15 (*Takeout Menu*) seguía activa (`is_visible: true`) con el slug `/chaats/`, pero existía una regla 301 redirigiendo `/chaats/` hacia la página `/menu/`.
* **Impacto en Google:** Google exige que los sitemaps contengan **únicamente URLs canónicas finales con respuesta HTTP 200**. Al encontrar una redirección en el sitemap, GSC emite alertas del tipo:
  > *"URL enviada tiene un problema: Redirección"* (*Submitted URL is a redirect*).

---

## 2. Acciones y Reparaciones Implementadas

### Solución A: Creación de Redirección 301 para `/sitemap.xml`
Se implementó una regla de redirección permanente en BigCommerce para capturar cualquier solicitud externa o bot que busque `sitemap.xml`:
* **Origen:** `https://qualitysweetsnj.com/sitemap.xml`
* **Destino:** `https://qualitysweetsnj.com/xmlsitemap.php`
* **Respuesta Actual en Vivo:** `HTTP 301 Moved Permanently` ➔ `https://qualitysweetsnj.com/xmlsitemap.php`.

### Solución B: Saneamiento de la Categoría `/chaats/` en BigCommerce API
Se archivó la categoría heredada 15 para excluirla del sitemap sin romper la redirección existente hacia el menú:
* `is_visible: false`
* `custom_url: /chaats-archived/`
* **Resultado:** BigCommerce eliminó inmediatamente `/chaats/` del sitemap de categorías. La redirección de usuarios antiguos `/chaats/` ➔ `/menu/` se mantiene 100% operativa.

---

## 3. Resultados de la Auditoría Completa (113 URLs Auditadas)

Se ejecutó un escaneo concurrente con cabecera oficial de Googlebot sobre cada una de las URLs presentes en todos los sitemaps:

| Métrica | Resultado | Estado |
| :--- | :---: | :---: |
| **Total de URLs en el Sitemap** | **113** | ✅ Conforme |
| **URLs con Respuesta HTTP 200 OK** | **113 (100%)** | ✅ Perfecto |
| **URLs con Redirección (3xx)** | **0** | ✅ Limpio |
| **URLs Rotas / Errores (4xx o 5xx)** | **0** | ✅ Sin caídas |
| **URLs con Directiva Noindex** | **0** | ✅ Indexables |
| **Discordancias de Canonical Tag** | **0** | ✅ Canónicas |

### Desglose por Sub-Sitemap:

1. **Páginas de Contenido (`type=pages&page=1`):**
   * Total: **13 URLs** (todas responden 200 OK).
   * Incluye: Home `/`, `/about-us`, `/menu/`, submenús `/menu/*`, `/locations/iselin-nj/`, políticas y blog.
2. **Productos del Catálogo (`type=products&page=1`):**
   * Total: **88 URLs** (todas responden 200 OK).
   * Dulces tradicionales, cajas de regalo, barfi, samosas y savories.
3. **Categorías Principales (`type=categories&page=1`):**
   * Total: **10 URLs** (todas responden 200 OK).
   * `/mithai-box/`, `/ready-made/`, `/indian-snacks/`, `/catering/`, `/traditional-mithai/`, `/barfi/`, `/indian-sweets/`, `/savories/`, `/bengali-sweets/`, `/custom/`.
4. **Artículos de Noticias / Blog (`type=news&page=1`):**
   * Total: **2 URLs** (todas responden 200 OK).

---

## 4. Verificación de `robots.txt`

El archivo `https://qualitysweetsnj.com/robots.txt` responde con **HTTP 200 OK** y declara correctamente el sitemap al final del archivo:

```txt
Sitemap: https://qualitysweetsnj.com/xmlsitemap.php
```

No hay bloqueos indebidos para Googlebot ni directivas que impidan el rastreo del catálogo.

---

## 5. Instrucciones Exactas para Google Search Console

Para que Google Search Console procese el sitemap sin errores:

1. **Entra a Google Search Console** y selecciona la propiedad `qualitysweetsnj.com`.
2. En el menú lateral izquierdo, haz clic en **Sitemaps** (dentro de la sección *Indexación*).
3. Si tienes una entrada antigua para `sitemap.xml` que dice *"No se ha podido recuperar"*:
   * Haz clic sobre ella.
   * Haz clic en los tres puntos verticales en la esquina superior derecha y selecciona **"Eliminar sitemap"**.
4. En el campo **"Añadir un nuevo sitemap"**, introduce exactamente:
   ```text
   xmlsitemap.php
   ```
   y pulsa **Enviar**.
5. *(Opcional pero muy recomendado en BigCommerce)* Puedes añadir también los sub-sitemaps individuales para acelerar el rastreo de productos y categorías de forma independiente:
   * `xmlsitemap.php?type=products&page=1`
   * `xmlsitemap.php?type=categories&page=1`
   * `xmlsitemap.php?type=pages&page=1`

> **Nota sobre Google Search Console:** En sitemaps tipo índice, a veces Google muestra inicialmente *"No se ha podido recuperar"* durante unos minutos o un par de horas mientras programa el rastreador en cola. Si esto ocurre, no te preocupes: el archivo responde HTTP 200 verificado y Google lo leerá en su próximo ciclo de rastreo.
