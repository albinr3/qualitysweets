import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Paths
BASE_DIR = Path(r"c:\Users\Albin Rodriguez\Documents\QualitySweets")
BASELINE = BASE_DIR / "baseline"
HEATMAP = Path(r"C:\Users\Albin Rodriguez\Downloads\Mapa de calor SEO en Nueva Jersey.png")

OUTPUT_DOCX = BASE_DIR / "outputs" / "docx" / "Quality_Sweets_First_Month_Progress_Report_September_2026.docx"
OUTPUT_SAME_DIR = BASE_DIR / "outputs" / "pdf" / "Quality_Sweets_First_Month_Progress_Report_September_2026.docx"

# Color constants
NAVY = "24323D"
SAFFRON = "C9851C"
GOLD = "F8F0DE"
BLUE = "EDF3F6"
GREEN = "EAF3EC"
GREY = "F3F4F6"
MID = "6B7280"
DARK = "2F3A42"
BORDER = "D9D9D9"
WHITE = "FFFFFF"
SUCCESS_GREEN = "2E7D32"

def set_cell_shading(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd')
        tcPr.append(shd)
    shd.set(qn('w:fill'), fill_hex)

def set_cell_border(cell, color=BORDER, size='6'):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    borders = tcPr.first_child_found_in('w:tcBorders')
    if borders is None:
        borders = OxmlElement('w:tcBorders')
        tcPr.append(borders)
    for edge in ('top', 'left', 'bottom', 'right'):
        tag = 'w:' + edge
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn('w:val'), 'single')
        element.set(qn('w:sz'), size)
        element.set(qn('w:color'), color)

def set_cell_margins(cell, top=100, start=120, bottom=100, end=120):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in('w:tcMar')
    if tcMar is None:
        tcMar = OxmlElement('w:tcMar')
        tcPr.append(tcMar)
    for m, v in [('top', top), ('start', start), ('bottom', bottom), ('end', end)]:
        node = tcMar.find(qn('w:' + m))
        if node is None:
            node = OxmlElement('w:' + m)
            tcMar.append(node)
        node.set(qn('w:w'), str(v))
        node.set(qn('w:type'), 'dxa')

def set_col_width(cell, inches):
    cell.width = Inches(inches)
    tcPr = cell._tc.get_or_add_tcPr()
    tcW = tcPr.find(qn('w:tcW'))
    if tcW is None:
        tcW = OxmlElement('w:tcW')
        tcPr.append(tcW)
    tcW.set(qn('w:w'), str(int(inches * 1440)))
    tcW.set(qn('w:type'), 'dxa')

def add_run(p, text, size=10, bold=False, color='000000', name='Helvetica'):
    r = p.add_run(text)
    r.font.name = name
    r._element.rPr.rFonts.set(qn('w:ascii'), name)
    r._element.rPr.rFonts.set(qn('w:hAnsi'), name)
    r.font.size = Pt(size)
    r.bold = bold
    r.font.color.rgb = RGBColor.from_string(color)
    return r

def add_bullet(doc, title, desc, size=9.2):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.16)
    p.paragraph_format.space_before = Pt(1.5)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.08
    add_run(p, title + ": ", size, True, NAVY)
    add_run(p, desc, size, False, DARK)
    return p

def create_table_row(table, col_widths, texts, fills=None, alignments=None, bolds=None, text_colors=None, font_sizes=None):
    cells = table.add_row().cells
    for i, cell in enumerate(cells):
        set_col_width(cell, col_widths[i])
        set_cell_border(cell, BORDER, '6')
        set_cell_margins(cell, top=80, start=100, bottom=80, end=100)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        if fills and i < len(fills) and fills[i]:
            set_cell_shading(cell, fills[i])
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        if alignments and i < len(alignments):
            p.alignment = alignments[i]
        bold = bolds[i] if bolds and i < len(bolds) else False
        color = text_colors[i] if text_colors and i < len(text_colors) else DARK
        size = font_sizes[i] if font_sizes and i < len(font_sizes) else 8.7
        add_run(p, texts[i], size, bold, color)
    return cells

def build_expanded_report():
    doc = Document()

    # Page setup
    sec = doc.sections[0]
    sec.top_margin = Inches(0.55)
    sec.bottom_margin = Inches(0.58)
    sec.left_margin = Inches(0.65)
    sec.right_margin = Inches(0.65)
    sec.different_first_page_header_footer = False

    # Header & Footer
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.paragraph_format.space_after = Pt(0)
    add_run(hp, "QUALITY SWEETS  |  COMPREHENSIVE FIRST MONTH REPORT", 7.4, True, MID)

    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.paragraph_format.space_before = Pt(4)
    fp.paragraph_format.space_after = Pt(0)
    add_run(fp, "Quality Sweets (1384 Oak Tree Rd, Iselin, NJ)  |  SEO & Digital Infrastructure Implementation  |  September 2026", 7.2, False, MID)

    # ==================== PAGE 1: EXECUTIVE SUMMARY & STATS ====================
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    add_run(p_title, "First Month Comprehensive Implementation Report", 21, True, "000000")

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(6)
    add_run(p_sub, "Quality Sweets — Local SEO, E-Commerce Infrastructure & Market Launch  |  September 2026", 10.5, True, SAFFRON)

    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.space_after = Pt(8)
    p_intro.paragraph_format.line_spacing = 1.15
    add_run(p_intro,
            "During this first month, our primary objective was establishing an unshakeable digital foundation for Quality Sweets. "
            "Rather than simple surface-level tweaks, we executed a complete architectural, technical, and operational overhaul across "
            "BigCommerce, Google Business Profile, Google Analytics 4, and Google Search Console. Extensive work was completed "
            "to clean up legacy technical debt, align online ordering paths, build out high-intent local and catering pages, and wire accurate "
            "conversion tracking so that every subsequent month can be measured with statistical certainty.",
            9.7, False, DARK)

    # 3 Metric Highlight Cards in Table
    stat_table = doc.add_table(rows=1, cols=3)
    stat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    stat_table.autofit = False
    stat_widths = [2.3, 2.3, 2.3]
    stats_data = [
        ("8", "New & Revamped Pages", "Homepage, /menu/ + 3 subpages, /catering/ + 3 subpages, /locations/iselin-nj/", BLUE),
        ("8", "Pickup Slugs Sanitized", "Eliminated duplicate URLs & 404 risks for delicate sweets", GREEN),
        ("8", "Baseline Geo-Grids", "8 local Google Maps geo-grids across core tracked keywords", GREY),
    ]
    for i, (num, label, desc, bg) in enumerate(stats_data):
        c = stat_table.cell(0, i)
        set_col_width(c, stat_widths[i])
        set_cell_shading(c, bg)
        set_cell_border(c, BORDER, '6')
        set_cell_margins(c, top=80, start=80, bottom=80, end=80)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cp = c.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_after = Pt(1)
        add_run(cp, num, 16, True, NAVY)
        cp2 = c.add_paragraph()
        cp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp2.paragraph_format.space_after = Pt(2)
        add_run(cp2, label, 8.8, True, DARK)
        cp3 = c.add_paragraph()
        cp3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp3.paragraph_format.space_after = Pt(0)
        cp3.paragraph_format.line_spacing = 1.02
        add_run(cp3, desc, 7.5, False, MID)

    # Section: Core Strategic Pillars Put In Place
    p_h2 = doc.add_paragraph()
    p_h2.paragraph_format.space_before = Pt(10)
    p_h2.paragraph_format.space_after = Pt(4)
    add_run(p_h2, "Key Strategic Pillars Put in Place", 12, True, "000000")

    cards_table = doc.add_table(rows=2, cols=2)
    cards_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cards_table.autofit = False
    cards_data = [
        ("1. Architecture & Triage Journey",
         "Transformed the website from a confusing single-flow catalogue into a 3-way triage hub: (1) Nationwide Sweets Shipping, (2) Fast In-Store & Takeout Pickup, and (3) Large-Scale Corporate & Wedding Catering.",
         GOLD),
        ("2. Forensic URL & Catalogue Cleanup",
         "Sanitized root URLs to canonical 'Short SEO' structure, removed legacy theme redirects, and fixed 8 duplicate/in-store pickup product titles to eliminate crawl bloat and preserve link equity.",
         BLUE),
        ("3. Google Business Profile Dominance",
         "Sanitized exact NAP address, set primary category to 'Indian sweets shop', updated attributes (Dine-in: NO, Takeout: YES), and populated 10 service categories, active product catalogue, and to-go menu.",
         GREEN),
        ("4. Dual Schema & Action Measurement",
         "Deployed advanced LocalBusiness + OnlineStore JSON-LD schema, submitted clean XML sitemaps, and configured GA4/GSC tracking for calls, directions, online orders, and catering leads.",
         GREY)
    ]
    for idx, (ctitle, cbody, fill) in enumerate(cards_data):
        r = idx // 2
        c = idx % 2
        cell = cards_table.cell(r, c)
        set_col_width(cell, 3.45)
        set_cell_shading(cell, fill)
        set_cell_border(cell, BORDER, '6')
        set_cell_margins(cell, top=90, start=110, bottom=90, end=110)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cp = cell.paragraphs[0]
        cp.paragraph_format.space_after = Pt(1.5)
        add_run(cp, ctitle, 9.3, True, NAVY)
        cp2 = cell.add_paragraph()
        cp2.paragraph_format.space_after = Pt(0)
        cp2.paragraph_format.line_spacing = 1.05
        add_run(cp2, cbody, 8.4, False, "374151")

    p_fnote1 = doc.add_paragraph()
    p_fnote1.paragraph_format.space_before = Pt(8)
    p_fnote1.paragraph_format.space_after = Pt(0)
    add_run(p_fnote1, "Detailed breakdown of all completed operational phases and technical deliverables follows on subsequent pages.", 8.5, True, SAFFRON)

    # ==================== PAGE 2: DETAILED TASK BREAKDOWN (PHASE 1 & PHASE 2) ====================
    doc.add_page_break()

    p_h2 = doc.add_paragraph()
    p_h2.paragraph_format.space_before = Pt(2)
    p_h2.paragraph_format.space_after = Pt(4)
    add_run(p_h2, "1. Forensic Technical Audit & Catalogue Sanitization (Phase 1)", 12.5, True, NAVY)

    p_desc = doc.add_paragraph()
    p_desc.paragraph_format.space_after = Pt(6)
    p_desc.paragraph_format.line_spacing = 1.1
    add_run(p_desc,
            "Quality Sweets had inherited significant technical legacy debt from older themes (Megnor) and default BigCommerce URL parameters. "
            "We conducted a forensic cleanup to eliminate 404 errors, consolidate redirect chains, and sanitize product naming conventions.",
            9.2, False, DARK)

    t1 = doc.add_table(rows=1, cols=3)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1.autofit = False
    w1 = [1.2, 4.2, 1.5]
    for i, h in enumerate(["Workstream", "Specific Tasks & Technical Actions Completed", "Status"]):
        c = t1.cell(0, i)
        set_col_width(c, w1[i])
        set_cell_shading(c, NAVY)
        set_cell_border(c, NAVY)
        set_cell_margins(c, 80, 100, 80, 100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 2 else WD_ALIGN_PARAGRAPH.LEFT
        add_run(p, h, 8.5, True, WHITE)

    t1_rows = [
        ("URL Structure & Canonicalization",
         "Configured 'SEO Optimized (Short)' in BigCommerce Store Setup. Renamed categories and slugs via REST API (IDs 3, 8, 22, 2, 1, 14, 21) into clean root paths, eliminating duplicate folder levels.",
         "DONE", GOLD),
        ("Forensic 301 Redirects",
         "Audited HTTP responses across core routes. Removed legacy Megnor demo redirect clutter and injected permanent 301 redirects mapping legacy paths (e.g., /bulk-corporate-orders/ to /catering/) to protect domain equity.",
         "DONE", BLUE),
        ("8 In-Store Pickup Slugs Sanitized",
         "Updated Product IDs 120 (Channa Mango Malai), 83 (Palki), 88 (Rose Chum Chum), 87 (Pineapple Chum Chum), 84 (Malai Chum Chum), 133 (Cherry Chum Chum), 78 (Manpasand), and 80 (Anarkali) with clean slugs.",
         "DONE", GREEN),
        ("Fulfillment & Pickup Rules",
         "Created dedicated 'Local Store Pickup Zone' (Free pickup at 1384 Oak Tree Rd, Iselin). Flagged delicate items (chaats, fresh chum chums) as 'In-Store Pickup Only' with clear frontend badges to prevent out-of-state shipping issues.",
         "DONE", GREY),
        ("Robots.txt & XML Sitemap",
         "Injected canonical sitemap declaration in robots.txt. Created and submitted clean XML sitemap to Google Search Console with 0 errors, validating crawl paths for search engine spiders.",
         "DONE", GOLD),
    ]
    for ws, action, st, fill in t1_rows:
        create_table_row(t1, w1, [ws, action, st], fills=[fill, WHITE, fill],
                         alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER],
                         bolds=[True, False, True], text_colors=[NAVY, DARK, SUCCESS_GREEN], font_sizes=[8.3, 8.2, 8.2])

    # Section 2: Website Deployment & On-Page SEO (Phase 2)
    p_h2 = doc.add_paragraph()
    p_h2.paragraph_format.space_before = Pt(10)
    p_h2.paragraph_format.space_after = Pt(4)
    add_run(p_h2, "2. Conversion Architecture & Content Implementation (Phase 2)", 12.5, True, NAVY)

    p_desc2 = doc.add_paragraph()
    p_desc2.paragraph_format.space_after = Pt(6)
    p_desc2.paragraph_format.line_spacing = 1.1
    add_run(p_desc2,
            "We built out high-converting dedicated pages to capture different customer intents: nationwide gift buyers, local takeout diners, and corporate/wedding event planners.",
            9.2, False, DARK)

    t2 = doc.add_table(rows=1, cols=3)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2.autofit = False
    for i, h in enumerate(["Target Page / Asset", "Implementation & SEO Strategy Delivered", "Status"]):
        c = t2.cell(0, i)
        set_col_width(c, w1[i])
        set_cell_shading(c, NAVY)
        set_cell_border(c, NAVY)
        set_cell_margins(c, 80, 100, 80, 100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 2 else WD_ALIGN_PARAGRAPH.LEFT
        add_run(p, h, 8.5, True, WHITE)

    t2_rows = [
        ("Homepage (Master Hub)",
         "Optimized Title, Meta Description & H1. Implemented 3-way triage CTAs (Shipping, Takeout, Catering), trust badges, dual store telephone click-to-call, and direct pickup ordering CTAs.",
         "DONE", GOLD),
        ("Takeout Digital Menu (/menu/)",
         "Launched official takeout menu hub with prominent 'Counter Pickup Only - No Dine-In' disclaimer. Created 3 dedicated sub-pages: /menu/chaats/ ('chaat near me'), /menu/street-food-snacks/ ('samosa near me', 'pani puri near me'), and /menu/drinks/.",
         "DONE", BLUE),
        ("Iselin Local Store Page (/locations/iselin-nj/)",
         "Published hyper-local landing page with verified NAP (1384 Oak Tree Rd), 7-day operating hours (10am-8pm), MetroPark NYC transit directions, parking guide, and fresh storefront photography.",
         "DONE", GREEN),
        ("B2B Catering Hub (/catering/)",
         "Migrated legacy /pages.php?pageid=4 to modern /catering/ hub. Integrated corporate inquiry form and Wedding Tasting Box selector. Deployed 3 specialized sub-landings: /wedding-catering-tri-state/, /temple-mandir-bulk-prasad/, and /bulk-samosa-orders/.",
         "DONE", GREY),
        ("6 E-Commerce Categories Copywriting",
         "Wrote 400+ words of keyword-targeted copy and structured FAQs for top retail categories: /indian-sweets/, /bengali-sweets/, /barfi/, /traditional-mithai/, /indian-snacks/, and /mithai-box/.",
         "DONE", GOLD),
    ]
    for ws, action, st, fill in t2_rows:
        create_table_row(t2, w1, [ws, action, st], fills=[fill, WHITE, fill],
                         alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER],
                         bolds=[True, False, True], text_colors=[NAVY, DARK, SUCCESS_GREEN], font_sizes=[8.3, 8.2, 8.2])

    # ==================== PAGE 3: SCHEMA, GBP, TRACKING & ROADMAP ====================
    doc.add_page_break()

    p_h2 = doc.add_paragraph()
    p_h2.paragraph_format.space_before = Pt(2)
    p_h2.paragraph_format.space_after = Pt(4)
    add_run(p_h2, "3. Structured Data, Google Profile & Analytics Setup (Phases 3 & 4)", 12.5, True, NAVY)

    t3 = doc.add_table(rows=1, cols=3)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3.autofit = False
    for i, h in enumerate(["Area", "Configuration & Optimization Delivered", "Status"]):
        c = t3.cell(0, i)
        set_col_width(c, w1[i])
        set_cell_shading(c, NAVY)
        set_cell_border(c, NAVY)
        set_cell_margins(c, 80, 100, 80, 100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 2 else WD_ALIGN_PARAGRAPH.LEFT
        add_run(p, h, 8.5, True, WHITE)

    t3_rows = [
        ("Dual JSON-LD Schema",
         "Implemented LocalBusiness & Bakery schema (geo-coordinates, official menu link, acceptsReservations: false), OnlineStore & Product schema (prices, stock, shipping), and BreadcrumbList across all pages.",
         "DONE", GOLD),
        ("Google Business Profile (GBP)",
         "Sanitized NAP address (1384 Oak Tree Rd). Set primary category to 'Indian sweets shop' and secondaries (Indian takeaway, Vegetarian restaurant, Caterer). Crafted 750-char SEO description. Set Dine-in to NO and Takeout to YES.",
         "DONE", GREEN),
        ("GBP Catalogue & Menu Items",
         "Configured 10 distinct GBP service categories. Uploaded active product catalogue with high-res photos and direct links. Embedded to-go takeout items directly into Google's native menu interface.",
         "DONE", BLUE),
        ("Google Shopping Free Listings",
         "Connected store product feed to Google Merchant Center, activating eligible retail sweets, snacks, and festive gift boxes for organic Google Shopping discovery.",
         "DONE", GREY),
        ("GA4 & Conversion Tracking",
         "Configured custom conversion events in Google Analytics 4 and GSC for primary commercial actions: phone calls, direction requests, online orders, catering lead submissions, and checkouts.",
         "DONE", GOLD),
        ("Keyword Tracking Project",
         "Configured Ubersuggest tracking project monitoring top 15-20 core keywords (mithai, chaat, samosas, catering) to capture accurate month-over-month position shifts.",
         "DONE", BLUE),
    ]
    for ws, action, st, fill in t3_rows:
        create_table_row(t3, w1, [ws, action, st], fills=[fill, WHITE, fill],
                         alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER],
                         bolds=[True, False, True], text_colors=[NAVY, DARK, SUCCESS_GREEN], font_sizes=[8.3, 8.2, 8.2])

    # Section 4: Performance Explanation & Month 2 Roadmap
    p_h2 = doc.add_paragraph()
    p_h2.paragraph_format.space_before = Pt(10)
    p_h2.paragraph_format.space_after = Pt(4)
    add_run(p_h2, "Why Commercial Data Starts in Month 2 & Strategic Roadmap", 12.5, True, NAVY)

    p_exp = doc.add_paragraph()
    p_exp.paragraph_format.space_after = Pt(6)
    p_exp.paragraph_format.line_spacing = 1.12
    add_run(p_exp,
            "Sales, revenue, and lead percentage changes are intentionally not included in this first report. "
            "Month 1 was dedicated entirely to building and deploying the technical architecture, indexing the new pages, and establishing clean tracking. "
            "Google requires a full 30-day reporting cycle to crawl, index, and re-rank the sanitized URLs. "
            "Comparing Month 1 against past untracked periods would be statistically misleading; our next report (around November 1, 2026) will provide the first true comparable performance cycle.",
            9.1, False, DARK)

    p_h3 = doc.add_paragraph()
    p_h3.paragraph_format.space_before = Pt(4)
    p_h3.paragraph_format.space_after = Pt(3)
    add_run(p_h3, "Month 2 Strategic Roadmap (Upcoming Initiatives):", 10, True, SAFFRON)

    add_bullet(doc, "Phase 4.4 — Visual Assets & GBP Posts", "Deploy weekly high-resolution photography of fresh sweets, store displays, and regular Google Business Posts to drive engagement and local relevance.")
    add_bullet(doc, "Phase 4.5 — Ethical Review Engine", "Implement in-store physical review acceleration (counter QR code cards and packaging inserts) to increase Google review velocity from genuine store visitors.")
    add_bullet(doc, "Phase 4.6 — Local Citation Authority", "Audit and align NAP consistency across the top 40 local business directories (Yelp, Apple Maps, Bing Places, YellowPages, etc.).")
    add_bullet(doc, "Phase 5.1 & 5.2 — Seasonal Landings & GEO", "Deploy evergreen festive campaign landings (Diwali, Holi, Wedding Season) and optimize content for Generative Engine Optimization (ChatGPT, Perplexity, Google AI Overviews).")

    # ==================== PAGES 4 to 11: VISUAL ANNEX WITH COMMENTARY ====================
    screens = [
        ("Indian sweets shop near me", BASELINE / "Captura de pantalla 2026-10-03 163017.png",
         "Google Maps Local Grid Scan (Middlesex County)",
         "Baseline Scan: Tracks local visibility for core high-intent search. Shows strong top-3 positioning immediately around Oak Tree Road with clear expansion opportunities into Edison and Woodbridge."),
        
        ("Indian sweets near me", BASELINE / "Captura de pantalla 2026-10-03 163116.png",
         "Google Maps Local Grid Scan (Middlesex County)",
         "Baseline Scan: Broad regional search for Indian sweets. Serves as our primary benchmark for local ranking gains following the GBP category sanitization."),
        
        ("Samosas near me", BASELINE / "Captura de pantalla 2026-10-03 163149.png",
         "Google Maps Local Grid Scan (Middlesex County)",
         "Baseline Scan: High-volume daily snack query. Supported by the newly deployed /menu/street-food-snacks/ page and to-go menu items added to Google."),
        
        ("Samosa chaat near me", BASELINE / "Captura de pantalla 2026-10-03 163212.png",
         "Google Maps Local Grid Scan (Middlesex County)",
         "Baseline Scan: Niche chaat query. Directly aligned with our new /menu/chaats/ sub-page to drive foot traffic for afternoon and evening snack runs."),
        
        ("Chaat near me", BASELINE / "Captura de pantalla 2026-10-03 163257.png",
         "Google Maps Local Grid Scan (Middlesex County)",
         "Baseline Scan: High-competition local search across Central NJ. Targeted via takeout menu architecture and GBP 'Vegetarian restaurant / Indian takeaway' categories."),
        
        ("Bengali sweets", BASELINE / "Captura de pantalla 2026-10-03 163320.png",
         "Google Maps Local Grid Scan (Middlesex County)",
         "Baseline Scan: Specialty mithai search. Directly targeted through the sanitized Bengali sweet product slugs (chum chums, palki, anarkali) and the optimized /bengali-sweets/ category copy."),
        
        ("Pani puri near me", BASELINE / "Captura de pantalla 2026-10-03 163354.png",
         "Google Maps Local Grid Scan (Middlesex County)",
         "Baseline Scan: Popular street food snack search. Tracks conversion to store visits via the updated takeout menu and call-to-order CTAs."),
        
        ("Jalebi near me", HEATMAP,
         "Google Maps Local Grid Scan (Middlesex County)",
         "Baseline Scan: High-intent traditional mithai search. Tracks initial local rankings for Jalebi across the Iselin and Central Jersey corridor as a baseline for ongoing optimization.")
    ]

    for title_text, img_path, subtitle_text, notes in screens:
        doc.add_page_break()

        # Title
        p_t = doc.add_paragraph()
        p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_t.paragraph_format.space_before = Pt(2)
        p_t.paragraph_format.space_after = Pt(2)
        add_run(p_t, title_text, 17, True, "000000")

        # Subtitle
        p_s = doc.add_paragraph()
        p_s.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_s.paragraph_format.space_after = Pt(8)
        add_run(p_s, subtitle_text, 9.2, True, SAFFRON)

        # Image
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(str(img_path), width=Inches(6.8))

        # Commentary Box / Table
        t_note = doc.add_table(rows=1, cols=1)
        t_note.alignment = WD_TABLE_ALIGNMENT.CENTER
        t_note.autofit = False
        c_note = t_note.cell(0, 0)
        set_col_width(c_note, 6.8)
        set_cell_shading(c_note, GREY)
        set_cell_border(c_note, BORDER, '6')
        set_cell_margins(c_note, top=70, start=100, bottom=70, end=100)
        p_nc = c_note.paragraphs[0]
        p_nc.paragraph_format.space_after = Pt(0)
        p_nc.paragraph_format.line_spacing = 1.05
        add_run(p_nc, "Strategic Analysis & Baseline Context: ", 8.2, True, NAVY)
        add_run(p_nc, notes, 8.1, False, DARK)

    # Save to outputs/docx
    OUTPUT_DOCX.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUTPUT_DOCX))
    print(f"Saved expanded DOCX: {OUTPUT_DOCX}")

    try:
        OUTPUT_SAME_DIR.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(OUTPUT_SAME_DIR))
        print(f"Saved expanded DOCX copy: {OUTPUT_SAME_DIR}")
    except PermissionError:
        alt_path = BASE_DIR / "outputs" / "pdf" / "Quality_Sweets_First_Month_Progress_Report_September_2026_v2.docx"
        doc.save(str(alt_path))
        print(f"File was locked by Word. Saved copy to: {alt_path}")

if __name__ == "__main__":
    build_expanded_report()
