import csv

with open('Keyword-Research-QualitySweets.csv', mode='r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# Define matching rules for clusters
clusters = {
    'Cluster 1: Homepage Master Hub & Marca': {
        'url': '/',
        'role': 'Master Hub, Triage Híbrido, Autoridad Principal',
        'keywords': []
    },
    'Cluster 2: Local Iselin & Regional Takeout': {
        'url': '/locations/iselin-nj/',
        'role': 'Landing Local de Tienda Física (Takeout Only, Oak Tree Rd)',
        'keywords': []
    },
    'Cluster 3: Comida Caliente, Samosas & Chaats (Takeout)': {
        'url': '/menu/ (y sub-silos /menu/chaats/, /menu/street-food-snacks/)',
        'role': 'Carta de Mostrador y Comida para Llevar',
        'keywords': []
    },
    'Cluster 4: E-Commerce Colección Madre (All Sweets)': {
        'url': '/indian-sweets/',
        'role': 'Catálogo Maestro de Dulces Frescos (52 variedades) con Envío USA',
        'keywords': []
    },
    'Cluster 5: Subcategoría Bengali Sweets': {
        'url': '/bengali-sweets/',
        'role': 'Especialidades de Chhena (Chum Chum, Rasgulla, Sandesh, Kalakand)',
        'keywords': []
    },
    'Cluster 6: Subcategoría Barfi & Kaju Katli': {
        'url': '/barfi/',
        'role': 'Kaju Katli puro, Barfi tradicional y Milk Cake',
        'keywords': []
    },
    'Cluster 7: Subcategoría Traditional Mithai': {
        'url': '/traditional-mithai/',
        'role': 'Ladoos, Jalebi caliente/fresco, Pedas, Gulab Jamun, Gujia',
        'keywords': []
    },
    'Cluster 8: Colección Indian Snacks & Namkeen': {
        'url': '/indian-snacks/',
        'role': 'Snacks secos, Mathi, Namak Para, Sev y frutos secos',
        'keywords': []
    },
    'Cluster 9: Cajas de Regalo, Festividades & B2B Catering': {
        'url': '/mithai-box/ & /catering/ & /seasonal/diwali-sweets-online/',
        'role': 'Cajas festivas, Catering de bodas, Mandirs y pedidos por volumen',
        'keywords': []
    }
}

for r in rows:
    kw = r['Keyword'].strip()
    kw_l = kw.lower()
    vol = int(r['Volume'])
    cpc = float(r['CPC']) if r['CPC'] else 0.0
    diff = int(r['SEO Difficulty']) if r['SEO Difficulty'] else 0
    item = {'Keyword': kw, 'Volume': vol, 'CPC': cpc, 'Difficulty': diff, 'Paid_Diff': r['Paid Difficulty']}
    
    # Matching logic
    if any(x in kw_l for x in ['catering', 'bulk samosa', 'samosa bulk', 'bulk mithai', 'bulk indian sweets', 'party catering', 'wedding']):
        clusters['Cluster 9: Cajas de Regalo, Festividades & B2B Catering']['keywords'].append(item)
    elif any(x in kw_l for x in ['diwali', 'gift box', 'gift basket', 'assorted sweets box']):
        clusters['Cluster 9: Cajas de Regalo, Festividades & B2B Catering']['keywords'].append(item)
    elif any(x in kw_l for x in ['iselin', 'edison', 'new jersey']) or (('near me' in kw_l or 'near' in kw_l) and any(y in kw_l for y in ['sweets', 'mithai', 'dessert', 'store', 'shop'])):
        clusters['Cluster 2: Local Iselin & Regional Takeout']['keywords'].append(item)
    elif any(x in kw_l for x in ['pani puri', 'chaat', 'bhatura', 'dahi bhalla', 'dahi puri', 'pakora', 'kachori', 'paratha', 'street food', 'samosa']):
        clusters['Cluster 3: Comida Caliente, Samosas & Chaats (Takeout)']['keywords'].append(item)
    elif any(x in kw_l for x in ['bengali', 'chum chum', 'cham cham', 'chomchom', 'rasgulla', 'sandesh']):
        clusters['Cluster 5: Subcategoría Bengali Sweets']['keywords'].append(item)
    elif any(x in kw_l for x in ['barfi', 'burfi', 'kaju katli', 'kalakand']):
        clusters['Cluster 6: Subcategoría Barfi & Kaju Katli']['keywords'].append(item)
    elif any(x in kw_l for x in ['ladoo', 'laddu', 'jalebi', 'peda', 'mithai', 'dessert']):
        clusters['Cluster 7: Subcategoría Traditional Mithai']['keywords'].append(item)
    elif any(x in kw_l for x in ['snack', 'savory', 'savories', 'mathi', 'namak para', 'sev', 'dhokla']):
        clusters['Cluster 8: Colección Indian Snacks & Namkeen']['keywords'].append(item)
    elif any(x in kw_l for x in ['order online', 'delivery to usa', 'usa delivery', 'online sweets']):
        clusters['Cluster 4: E-Commerce Colección Madre (All Sweets)']['keywords'].append(item)
    else:
        clusters['Cluster 1: Homepage Master Hub & Marca']['keywords'].append(item)

total_count = sum(len(c['keywords']) for c in clusters.values())
total_vol = sum(sum(k['Volume'] for k in c['keywords']) for c in clusters.values())
print(f"Total Palabras Clave Mapeadas: {total_count} de {len(rows)}")
print(f"Volumen Total Mensual: {total_vol:,}")

for name, data in clusters.items():
    c_vol = sum(k['Volume'] for k in data['keywords'])
    print(f"\n### {name} ({len(data['keywords'])} keywords | {c_vol:,} vol/mes)")
    print(f"URL Canónica: {data['url']}")
    data['keywords'].sort(key=lambda x: -x['Volume'])
    for k in data['keywords']:
        print(f"  - {k['Keyword']} | Vol: {k['Volume']:,} | CPC: ${k['CPC']:.2f} | KD: {k['Difficulty']}")
