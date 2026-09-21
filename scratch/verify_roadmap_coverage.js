const fs = require('fs');
const tasks = JSON.parse(fs.readFileSync('scratch/bonsai_tasks.json', 'utf8'));
const qsTasks = tasks.filter(t => t.project_id === 1535714);

const roadmapSteps = [
  {
    phase: 'Fase 1: Saneamiento Técnico de BigCommerce y Redirecciones 301',
    steps: [
      {
        id: '1.1',
        title: 'Paso 1.1: Configuración de URLs en Raíz ("SEO Optimized Short") y Renombrado de Categorías',
        expected_status: 'Done',
        parent_task: 'TSK-01102',
        subtasks: ['TSK-01103', 'TSK-01104']
      },
      {
        id: '1.2',
        title: 'Paso 1.2: Auditoría Forense y Verificación de Redirecciones 301 en Vivo',
        expected_status: 'Done',
        parent_task: 'TSK-01105',
        subtasks: ['TSK-01106', 'TSK-01107', 'TSK-01108']
      },
      {
        id: '1.3',
        title: 'Paso 1.3: Saneamiento Inmediato de Fichas de Producto y Slugs (Product IDs)',
        expected_status: 'Done',
        parent_task: 'TSK-01109',
        subtasks: ['TSK-01110', 'TSK-01111', 'TSK-01112', 'TSK-01113', 'TSK-01114', 'TSK-01115', 'TSK-01116', 'TSK-01117']
      },
      {
        id: '1.4',
        title: 'Paso 1.4: Configuración de Métodos de Envío y Zonas de Entrega',
        expected_status: 'Done',
        parent_task: 'TSK-01118',
        subtasks: ['TSK-01120', 'TSK-01121', 'TSK-01122']
      },
      {
        id: '1.5',
        title: 'Paso 1.5: Ajuste de Robots.txt y Sitemap XML',
        expected_status: 'Done',
        parent_task: 'TSK-01119',
        subtasks: ['TSK-01123', 'TSK-01124']
      }
    ]
  },
  {
    phase: 'Fase 2: Reestructuración de Páginas Clave y Contenido On-Page',
    steps: [
      {
        id: '2.1',
        title: 'Paso 2.1: Rediseño de la Homepage (Master Hub)',
        expected_status: 'Done',
        parent_task: 'TSK-01125',
        subtasks: ['TSK-01130', 'TSK-01131', 'TSK-01132', 'TSK-01133']
      },
      {
        id: '2.2',
        title: 'Paso 2.2: Carta Oficial de Takeout (/menu/) y Sub-silos',
        expected_status: 'Done',
        parent_task: 'TSK-01126',
        subtasks: ['TSK-01134', 'TSK-01135', 'TSK-01136', 'TSK-01137', 'TSK-01138']
      },
      {
        id: '2.3',
        title: 'Paso 2.3: Despliegue de la Landing Local (/locations/iselin-nj/)',
        expected_status: 'Done',
        parent_task: 'TSK-01127',
        subtasks: ['TSK-01139', 'TSK-01140', 'TSK-01141', 'TSK-01142']
      },
      {
        id: '2.4',
        title: 'Paso 2.4: Landing B2B y Catering Unificada (/catering/)',
        expected_status: 'Done',
        parent_task: 'TSK-01128',
        subtasks: ['TSK-01143', 'TSK-01144', 'TSK-01145', 'TSK-01146', 'TSK-01147']
      },
      {
        id: '2.5',
        title: 'Paso 2.5: Redacción On-Page de las 6 Categorías de E-commerce',
        expected_status: 'Done',
        parent_task: 'TSK-01129',
        subtasks: ['TSK-01148', 'TSK-01149', 'TSK-01150', 'TSK-01151', 'TSK-01152', 'TSK-01153']
      }
    ]
  },
  {
    phase: 'Fase 3: Marcado Estructurado Schema.org, Analítica y Google Merchant',
    steps: [
      {
        id: '3.1',
        title: 'Paso 3.1: Schema JSON-LD SSR mediante BigCommerce Blueprint',
        expected_status: 'Done',
        parent_task: 'TSK-01154',
        subtasks: ['TSK-01157', 'TSK-01158', 'TSK-01159']
      },
      {
        id: '3.2',
        title: 'Paso 3.2: Configuración de Analítica y Conversiones (GA4 & GSC)',
        expected_status: 'En Progreso (GA4 Done, GSC To Do)',
        parent_task: 'TSK-01155',
        subtasks: ['TSK-01160', 'TSK-01161']
      },
      {
        id: '3.3',
        title: 'Paso 3.3: Activación de Google Shopping (Merchant Center Free Listings)',
        expected_status: 'To Do',
        parent_task: 'TSK-01156',
        subtasks: ['TSK-01162', 'TSK-01163']
      }
    ]
  },
  {
    phase: 'Fase 4: Google Business Profile (GBP), Citaciones y Reputación Local',
    steps: [
      {
        id: '4.1',
        title: 'Paso 4.1: Entidad Local, NAP y Categorías Canónicas',
        expected_status: 'Done',
        parent_task: 'TSK-01164',
        subtasks: ['TSK-01168', 'TSK-01169', 'TSK-01170']
      },
      {
        id: '4.2',
        title: 'Paso 4.2: Descripción GBP SEO Local (750 caracteres)',
        expected_status: 'Done',
        parent_task: 'TSK-01647',
        subtasks: []
      },
      {
        id: '4.3',
        title: 'Paso 4.3: Configuración de Atributos y Servicios en GBP',
        expected_status: 'Done',
        parent_task: 'TSK-01165',
        subtasks: ['TSK-01171', 'TSK-01172', 'TSK-01643']
      },
      {
        id: '4.3B',
        title: 'Paso 4.3B: Productos GBP (Catálogo activo mithai y gift boxes)',
        expected_status: 'Done',
        parent_task: 'TSK-01644',
        subtasks: []
      },
      {
        id: '4.3C',
        title: 'Paso 4.3C: Menú Takeout GBP (Platos Preparados To-Go)',
        expected_status: 'Done',
        parent_task: 'TSK-01646',
        subtasks: []
      },
      {
        id: '4.4',
        title: 'Paso 4.4: Fotos, Video y Google Posts en Google Business Profile',
        expected_status: 'To Do',
        parent_task: 'TSK-01648',
        subtasks: ['TSK-01649', 'TSK-01650']
      },
      {
        id: '4.5',
        title: 'Paso 4.5: Motor Físico y Ético de Reseñas (In-Store QR & Packaging Cards)',
        expected_status: 'To Do',
        parent_task: 'TSK-01166',
        subtasks: ['TSK-01173', 'TSK-01174']
      },
      {
        id: '4.6',
        title: 'Paso 4.6: Citaciones Locales y Control Mensual (Top 40 Directories)',
        expected_status: 'To Do',
        parent_task: 'TSK-01167',
        subtasks: ['TSK-01175', 'TSK-01176']
      }
    ]
  },
  {
    phase: 'Fase 5: Expansión Regional B2B, Campañas Festivas y Motores de IA',
    steps: [
      {
        id: '5.1',
        title: 'Paso 5.1: Landings Estacionales Perennes (Diwali, Karwa Chauth, Holi)',
        expected_status: 'To Do',
        parent_task: 'TSK-01177',
        subtasks: ['TSK-01179', 'TSK-01180', 'TSK-01181']
      },
      {
        id: '5.2',
        title: 'Paso 5.2: Optimización para Motores de Inteligencia Artificial (GEO)',
        expected_status: 'To Do',
        parent_task: 'TSK-01178',
        subtasks: ['TSK-01182', 'TSK-01183']
      }
    ]
  }
];

console.log('=== AUDITORIA ROADMAP VS BONSAI TASKS ===\n');

let totalSteps = 0;
let totalMapped = 0;

roadmapSteps.forEach(phase => {
  console.log(`\n======================================================`);
  console.log(`📌 ${phase.phase}`);
  console.log(`======================================================`);

  phase.steps.forEach(step => {
    totalSteps++;
    const pTask = qsTasks.find(t => t.number === step.parent_task);
    if (!pTask) {
      console.log(`❌ [MISSING PARENT] ${step.id}: ${step.title}`);
      return;
    }
    totalMapped++;
    console.log(`\n✅ [${pTask.number}] "${pTask.title}"`);
    console.log(`   Estado Bonsai: ${pTask.task_status?.status} | Esperado Roadmap: ${step.expected_status}`);

    step.subtasks.forEach(sNum => {
      const sTask = qsTasks.find(t => t.number === sNum);
      if (!sTask) {
        console.log(`   ❌ [MISSING SUBTASK] ${sNum}`);
      } else {
        console.log(`      ├── [${sTask.number}] "${sTask.title}" -> ${sTask.task_status?.status}`);
      }
    });
  });
});

console.log(`\n------------------------------------------------------`);
console.log(`Total Pasos Auditados: ${totalSteps} | Mapeados 100% en Bonsai: ${totalMapped}`);
console.log(`------------------------------------------------------`);
