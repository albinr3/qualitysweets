import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Función para cargar .env si no vienen en process.env
function loadEnv() {
  const possiblePaths = [
    path.resolve(__dirname, "../../.env"),
    path.resolve(process.cwd(), ".env"),
    path.resolve(__dirname, ".env"),
  ];

  for (const envPath of possiblePaths) {
    if (fs.existsSync(envPath)) {
      const content = fs.readFileSync(envPath, "utf-8");
      for (const line of content.split("\n")) {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith("#") && trimmed.includes("=")) {
          const [k, ...v] = trimmed.split("=");
          const key = k.trim();
          const val = v.join("=").trim().replace(/^["']|["']$/g, "");
          if (!process.env[key]) {
            process.env[key] = val;
          }
        }
      }
      break;
    }
  }
}

loadEnv();

const STORE_HASH = process.env.BIGCOMMERCE_STORE_HASH;
const ACCESS_TOKEN = process.env.BIGCOMMERCE_ACCESS_TOKEN;
const CLIENT_ID = process.env.BIGCOMMERCE_CLIENT_ID;

if (!STORE_HASH || !ACCESS_TOKEN) {
  console.error("ERROR: BIGCOMMERCE_STORE_HASH and BIGCOMMERCE_ACCESS_TOKEN must be set.");
  process.exit(1);
}

const BASE_URL = `https://api.bigcommerce.com/stores/${STORE_HASH}`;

async function bcFetch(endpoint, options = {}) {
  const url = endpoint.startsWith("http") ? endpoint : `${BASE_URL}${endpoint}`;
  const headers = {
    "X-Auth-Token": ACCESS_TOKEN,
    Accept: "application/json",
    "Content-Type": "application/json",
    ...options.headers,
  };
  if (CLIENT_ID) {
    headers["X-Auth-Client"] = CLIENT_ID;
  }

  const res = await fetch(url, {
    ...options,
    headers,
  });

  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = text;
  }

  if (!res.ok) {
    const errorMsg = typeof data === "object" ? JSON.stringify(data) : data;
    throw new Error(`BigCommerce API Error (HTTP ${res.status}): ${errorMsg}`);
  }

  return data;
}

const server = new McpServer({
  name: "bigcommerce-admin-mcp",
  version: "1.0.0",
});

// 1. INFORMACIÓN DE LA TIENDA
server.tool("bc_get_store_info", "Obtiene la información general de la tienda BigCommerce (nombre, dominio, plan, estado).", {}, async () => {
  try {
    const data = await bcFetch("/v2/store");
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  } catch (err) {
    return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
  }
});

// 2. AJUSTES SEO GLOBALES
server.tool("bc_get_seo_settings", "Obtiene los ajustes SEO globales de la tienda (Title Tag de Home, Meta Description, Keywords).", {}, async () => {
  try {
    const data = await bcFetch("/v3/settings/storefront/seo");
    return { content: [{ type: "text", text: JSON.stringify(data.data || data, null, 2) }] };
  } catch (err) {
    return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
  }
});

server.tool(
  "bc_update_seo_settings",
  "Actualiza los ajustes SEO globales de la tienda (Title Tag de Home, Meta Description, Meta Keywords).",
  {
    page_title: z.string().optional().describe("Title Tag de la Home / Storefront"),
    meta_description: z.string().optional().describe("Meta Description de la Home"),
    meta_keywords: z.string().optional().describe("Meta Keywords globales"),
  },
  async (args) => {
    try {
      const payload = {};
      if (args.page_title !== undefined) payload.page_title = args.page_title;
      if (args.meta_description !== undefined) payload.meta_description = args.meta_description;
      if (args.meta_keywords !== undefined) payload.meta_keywords = args.meta_keywords;

      const data = await bcFetch("/v3/settings/storefront/seo", {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      return {
        content: [{ type: "text", text: `Ajustes SEO actualizados exitosamente:\n${JSON.stringify(data.data || data, null, 2)}` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
    }
  }
);

// 3. PÁGINAS WEB (CMS / CONTENT PAGES)
server.tool(
  "bc_list_pages",
  "Lista todas las páginas web de contenido (CMS) existentes en la tienda.",
  {
    channel_id: z.number().optional().describe("ID del canal si es multi-storefront (por defecto canal 1)"),
  },
  async (args) => {
    try {
      const query = args.channel_id ? `?channel_id=${args.channel_id}` : "";
      const data = await bcFetch(`/v3/content/pages${query}`);
      return { content: [{ type: "text", text: JSON.stringify(data.data || data, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
    }
  }
);

server.tool(
  "bc_get_page",
  "Obtiene todos los detalles y contenido HTML de una página web específica por su ID.",
  {
    page_id: z.number().describe("ID numérico de la página en BigCommerce"),
  },
  async (args) => {
    try {
      const data = await bcFetch(`/v3/content/pages/${args.page_id}`);
      return { content: [{ type: "text", text: JSON.stringify(data.data || data, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
    }
  }
);

server.tool(
  "bc_create_page",
  "Crea una nueva página web (CMS) en BigCommerce con contenido HTML y metadatos SEO.",
  {
    name: z.string().describe("Nombre de la página (visible en navegación)"),
    body: z.string().describe("Contenido HTML del cuerpo de la página"),
    url: z.string().optional().describe("URL relativa canónica (ej: /locations/iselin-nj/ o /catering/)"),
    type: z.enum(["raw", "page", "link", "blog"]).default("raw").describe("Tipo de página (normalmente 'raw' para HTML o 'page')"),
    is_visible: z.boolean().default(true).describe("Si se muestra o no en la barra de navegación"),
    parent_id: z.number().default(0).describe("ID de página padre si es subpágina (0 para raíz)"),
    meta_title: z.string().optional().describe("Título SEO (<title>) de la página"),
    meta_description: z.string().optional().describe("Meta descripción SEO de la página"),
    search_keywords: z.string().optional().describe("Palabras clave de búsqueda"),
  },
  async (args) => {
    try {
      const payload = {
        name: args.name,
        body: args.body,
        type: args.type || "raw",
        is_visible: args.is_visible ?? true,
        parent_id: args.parent_id ?? 0,
      };
      if (args.url) payload.url = args.url;
      if (args.meta_title) payload.meta_title = args.meta_title;
      if (args.meta_description) payload.meta_description = args.meta_description;
      if (args.search_keywords) payload.search_keywords = args.search_keywords;

      const data = await bcFetch("/v3/content/pages", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      return {
        content: [{ type: "text", text: `Página creada con éxito:\n${JSON.stringify(data.data || data, null, 2)}` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
    }
  }
);

server.tool(
  "bc_update_page",
  "Modifica una página web existente (contenido HTML, título, URL, SEO, visibilidad).",
  {
    page_id: z.number().describe("ID de la página a modificar"),
    name: z.string().optional().describe("Nuevo nombre de la página"),
    body: z.string().optional().describe("Nuevo contenido HTML"),
    url: z.string().optional().describe("Nueva URL relativa canónica"),
    is_visible: z.boolean().optional().describe("Visibilidad en el menú"),
    meta_title: z.string().optional().describe("Nuevo meta título SEO"),
    meta_description: z.string().optional().describe("Nueva meta descripción SEO"),
    search_keywords: z.string().optional().describe("Nuevas search keywords"),
  },
  async (args) => {
    try {
      const { page_id, ...updates } = args;
      const data = await bcFetch(`/v3/content/pages/${page_id}`, {
        method: "PUT",
        body: JSON.stringify(updates),
      });
      return {
        content: [{ type: "text", text: `Página ${page_id} actualizada con éxito:\n${JSON.stringify(data.data || data, null, 2)}` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
    }
  }
);

server.tool(
  "bc_delete_page",
  "Elimina una página web del CMS por su ID.",
  {
    page_id: z.number().describe("ID de la página a eliminar"),
  },
  async (args) => {
    try {
      await bcFetch(`/v3/content/pages/${args.page_id}`, { method: "DELETE" });
      return { content: [{ type: "text", text: `Página ${args.page_id} eliminada exitosamente.` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
    }
  }
);

// 4. CATEGORÍAS DEL CATÁLOGO
server.tool(
  "bc_list_categories",
  "Lista las categorías del catálogo con sus IDs, nombres, URLs (slugs) y SEO.",
  {
    limit: z.number().default(50).describe("Límite de categorías a obtener (por defecto 50)"),
    page: z.number().default(1).describe("Página de paginación"),
  },
  async (args) => {
    try {
      const data = await bcFetch(`/v3/catalog/categories?limit=${args.limit}&page=${args.page}`);
      return { content: [{ type: "text", text: JSON.stringify(data.data || data, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
    }
  }
);

server.tool(
  "bc_get_category",
  "Obtiene la información detallada de una categoría por su ID.",
  {
    category_id: z.number().describe("ID numérico de la categoría"),
  },
  async (args) => {
    try {
      const data = await bcFetch(`/v3/catalog/categories/${args.category_id}`);
      return { content: [{ type: "text", text: JSON.stringify(data.data || data, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
    }
  }
);

server.tool(
  "bc_update_category",
  "Actualiza el nombre, slug URL, descripción rica o metadatos SEO de una categoría.",
  {
    category_id: z.number().describe("ID de la categoría a actualizar"),
    name: z.string().optional().describe("Nuevo nombre de la categoría"),
    url: z.string().optional().describe("Nuevo slug canónico en raíz (ej: /indian-sweets/ o /bengali-sweets/)"),
    description: z.string().optional().describe("Texto o contenido HTML descriptivo de la categoría"),
    page_title: z.string().optional().describe("Title Tag SEO de la categoría"),
    meta_description: z.string().optional().describe("Meta descripción SEO de la categoría"),
    search_keywords: z.string().optional().describe("Search keywords"),
  },
  async (args) => {
    try {
      const payload = {};
      if (args.name !== undefined) payload.name = args.name;
      if (args.description !== undefined) payload.description = args.description;
      if (args.page_title !== undefined) payload.page_title = args.page_title;
      if (args.meta_description !== undefined) payload.meta_description = args.meta_description;
      if (args.search_keywords !== undefined) payload.search_keywords = args.search_keywords;
      if (args.url !== undefined) {
        payload.custom_url = {
          url: args.url,
          is_customized: true,
        };
      }

      const data = await bcFetch(`/v3/catalog/categories/${args.category_id}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });

      return {
        content: [{ type: "text", text: `Categoría ${args.category_id} actualizada exitosamente:\n${JSON.stringify(data.data || data, null, 2)}` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
    }
  }
);

// 5. PRODUCTOS (PARA SANEAMIENTO DE SLUGS Y NOMBRES)
server.tool(
  "bc_get_product",
  "Obtiene la información de un producto por su Product ID.",
  {
    product_id: z.number().describe("ID del producto"),
  },
  async (args) => {
    try {
      const data = await bcFetch(`/v3/catalog/products/${args.product_id}`);
      return { content: [{ type: "text", text: JSON.stringify(data.data || data, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
    }
  }
);

server.tool(
  "bc_update_product",
  "Actualiza el nombre, URL slug o SEO de un producto específico (ej: sanear productos pick-up).",
  {
    product_id: z.number().describe("ID numérico del producto"),
    name: z.string().optional().describe("Nuevo nombre limpio del producto"),
    url: z.string().optional().describe("Nuevo slug de URL canónica limpia"),
    page_title: z.string().optional().describe("SEO Page Title"),
    meta_description: z.string().optional().describe("SEO Meta Description"),
  },
  async (args) => {
    try {
      const payload = {};
      if (args.name !== undefined) payload.name = args.name;
      if (args.page_title !== undefined) payload.page_title = args.page_title;
      if (args.meta_description !== undefined) payload.meta_description = args.meta_description;
      if (args.url !== undefined) {
        payload.custom_url = {
          url: args.url,
          is_customized: true,
        };
      }

      const data = await bcFetch(`/v3/catalog/products/${args.product_id}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });

      return {
        content: [{ type: "text", text: `Producto ${args.product_id} actualizado con éxito:\n${JSON.stringify(data.data || data, null, 2)}` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
    }
  }
);

// 6. SCRIPTS / SCHEMA INJECTION
server.tool("bc_list_scripts", "Lista los scripts y códigos inyectados en la cabecera/pie de la tienda (Script Manager).", {}, async () => {
  try {
    const data = await bcFetch("/v3/content/scripts");
    return { content: [{ type: "text", text: JSON.stringify(data.data || data, null, 2) }] };
  } catch (err) {
    return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
  }
});

server.tool(
  "bc_create_script",
  "Inyecta un script HTML o marcado Schema.org JSON-LD en el head o footer de la tienda.",
  {
    name: z.string().describe("Nombre identificativo del script (ej: 'LocalBusiness Schema')"),
    html: z.string().describe("Contenido HTML exacto del script (incluyendo etiquetas <script>...</script>)"),
    location: z.enum(["head", "footer"]).default("head").describe("Ubicación de inyección"),
    visibility: z.enum(["all_pages", "storefront", "checkout", "order_confirmation"]).default("all_pages"),
    description: z.string().optional().describe("Descripción opcional"),
  },
  async (args) => {
    try {
      const payload = {
        name: args.name,
        html: args.html,
        location: args.location,
        visibility: args.visibility,
        kind: "script_tag",
        consent_category: "essential",
        description: args.description || "Injected via MCP",
      };

      const data = await bcFetch("/v3/content/scripts", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      return {
        content: [{ type: "text", text: `Script creado exitosamente:\n${JSON.stringify(data.data || data, null, 2)}` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
    }
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error("Fatal error starting BigCommerce MCP server:", err);
  process.exit(1);
});
