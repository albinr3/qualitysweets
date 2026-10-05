from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
)

BASE_DIR = Path(r"c:\Users\Albin Rodriguez\Documents\QualitySweets")
OUTPUT = BASE_DIR / "outputs" / "pdf" / "Quality_Sweets_First_Month_Progress_Report_September_2026.pdf"
BASELINE = BASE_DIR / "baseline"
HEATMAP = Path(r"C:\Users\Albin Rodriguez\Downloads\Mapa de calor SEO en Nueva Jersey.png")

NAVY = colors.HexColor('#24323D')
SAFFRON = colors.HexColor('#C9851C')
GOLD = colors.HexColor('#F8F0DE')
BLUE = colors.HexColor('#EDF3F6')
GREEN = colors.HexColor('#EAF3EC')
GREY = colors.HexColor('#F3F4F6')
MID = colors.HexColor('#6B7280')
DARK = colors.HexColor('#2F3A42')
BORDER = colors.HexColor('#D9D9D9')
SUCCESS = colors.HexColor('#2E7D32')
WHITE = colors.HexColor('#FFFFFF')
PAGE_W, PAGE_H = letter

def para(text, style):
    return Paragraph(text, style)

styles = getSampleStyleSheet()

# Typography Styles
title_style = ParagraphStyle('TitleStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=20,
                             leading=23, textColor=colors.black, spaceAfter=2)
sub_style = ParagraphStyle('SubStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5,
                           leading=12, textColor=SAFFRON, spaceAfter=5)
intro_style = ParagraphStyle('IntroStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=8.6,
                             leading=11.2, textColor=DARK, spaceAfter=6)
h2_style = ParagraphStyle('H2Style', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11,
                          leading=13.5, textColor=NAVY, spaceBefore=4, spaceAfter=3)
h3_style = ParagraphStyle('H3Style', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.2,
                          leading=11.5, textColor=SAFFRON, spaceBefore=3, spaceAfter=2)
body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5,
                            leading=10.8, textColor=DARK, spaceAfter=4)
bullet_style = ParagraphStyle('BulletStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=8.2,
                              leading=10.4, textColor=DARK, leftIndent=12, firstLineIndent=-8, spaceAfter=2)

stat_num_style = ParagraphStyle('StatNum', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15,
                                leading=17, textColor=NAVY, alignment=TA_CENTER)
stat_lbl_style = ParagraphStyle('StatLbl', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8,
                                leading=9.5, textColor=DARK, alignment=TA_CENTER)
stat_desc_style = ParagraphStyle('StatDesc', parent=styles['Normal'], fontName='Helvetica', fontSize=6.8,
                                 leading=8.2, textColor=MID, alignment=TA_CENTER)

card_title_style = ParagraphStyle('CardTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.8,
                                  leading=10.5, textColor=NAVY, spaceAfter=1)
card_body_style = ParagraphStyle('CardBody', parent=styles['Normal'], fontName='Helvetica', fontSize=7.8,
                                 leading=9.4, textColor=colors.HexColor('#374151'))

th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8,
                          leading=9.5, textColor=WHITE)
th_center = ParagraphStyle('THCenter', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8,
                           leading=9.5, textColor=WHITE, alignment=TA_CENTER)

td_cat_style = ParagraphStyle('TDCat', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.8,
                              leading=9.2, textColor=NAVY)
td_body_style = ParagraphStyle('TDBody', parent=styles['Normal'], fontName='Helvetica', fontSize=7.6,
                               leading=9.1, textColor=DARK)
td_status_style = ParagraphStyle('TDStatus', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.6,
                                 leading=9, textColor=SUCCESS, alignment=TA_CENTER)

keyword_title = ParagraphStyle('KeywordTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=17,
                               leading=20, textColor=colors.black, alignment=TA_CENTER, spaceAfter=2)
keyword_subtitle = ParagraphStyle('KeywordSubtitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9,
                                  leading=11, textColor=SAFFRON, alignment=TA_CENTER, spaceAfter=6)
note_title = ParagraphStyle('NoteTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.8,
                            leading=9.5, textColor=NAVY)
note_body = ParagraphStyle('NoteBody', parent=styles['Normal'], fontName='Helvetica', fontSize=7.8,
                           leading=9.8, textColor=DARK)

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MID)
    canvas.setFont('Helvetica-Bold', 7.4)
    canvas.drawRightString(PAGE_W - 0.65 * inch, PAGE_H - 0.36 * inch, 'QUALITY SWEETS  |  COMPREHENSIVE FIRST MONTH REPORT')
    canvas.setFont('Helvetica', 7.2)
    canvas.drawCentredString(PAGE_W / 2, 0.33 * inch, 'Quality Sweets (1384 Oak Tree Rd, Iselin, NJ)  |  SEO & Digital Infrastructure Implementation  |  September 2026')
    canvas.restoreState()

def build_table(headers, rows, col_widths, row_height=None):
    data = []
    # Header row
    h_cells = []
    for i, h in enumerate(headers):
        s = th_center if i == len(headers) - 1 else th_style
        h_cells.append(para(h, s))
    data.append(h_cells)
    
    # Body rows
    for cat, text, status, fill in rows:
        c_cat = para(cat, td_cat_style)
        c_text = para(text, td_body_style)
        c_stat = para(status, td_status_style)
        data.append([c_cat, c_text, c_stat])
    
    t = Table(data, colWidths=col_widths)
    t_style = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('BOX', (0, 0), (-1, -1), 0.35, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.35, BORDER),
    ]
    for r_idx, (_, _, _, fill) in enumerate(rows, start=1):
        t_style.append(('BACKGROUND', (0, r_idx), (0, r_idx), fill))
        t_style.append(('BACKGROUND', (1, r_idx), (1, r_idx), WHITE))
        t_style.append(('BACKGROUND', (2, r_idx), (2, r_idx), fill))
    t.setStyle(TableStyle(t_style))
    return t

def build_pdf():
    story = []

    # ==================== PAGE 1: EXECUTIVE SUMMARY & STATS ====================
    story.append(para("First Month Comprehensive Implementation Report", title_style))
    story.append(para("Quality Sweets — Local SEO, E-Commerce Infrastructure & Market Launch  |  September 2026", sub_style))
    story.append(para(
        "During this first month, our primary objective was establishing an unshakeable digital foundation for Quality Sweets. "
        "Rather than simple surface-level tweaks, we executed a complete architectural, technical, and operational overhaul across "
        "BigCommerce, Google Business Profile, Google Analytics 4, and Google Search Console. Extensive work was completed "
        "to clean up legacy technical debt, align online ordering paths, build out high-intent local and catering pages, and wire accurate "
        "conversion tracking so that every subsequent month can be measured with statistical certainty.",
        intro_style))

    # 3 Stat Cards
    stat_widths = [2.32 * inch, 2.32 * inch, 2.32 * inch]
    stat_cards = [
        Table([[para("8", stat_num_style)], [para("Pages Deployed", stat_lbl_style)], [para("Hub, /menu/ + 3 sub, /catering/ + 3 sub, /iselin/", stat_desc_style)]],
              colWidths=[2.28 * inch]),
        Table([[para("8", stat_num_style)], [para("Pickup Slugs Fixed", stat_lbl_style)], [para("Eliminated duplicate URLs & 404 risks", stat_desc_style)]],
              colWidths=[2.28 * inch]),
        Table([[para("8", stat_num_style)], [para("Baseline Geo-Grids", stat_lbl_style)], [para("8 local Google Maps geo-grids across core keywords", stat_desc_style)]],
              colWidths=[2.28 * inch]),
    ]
    for sc, bg in zip(stat_cards, [BLUE, GREEN, GREY]):
        sc.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg),
            ('BOX', (0, 0), (-1, -1), 0.35, BORDER),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))
    stat_grid = Table([[stat_cards[0], stat_cards[1], stat_cards[2]]], colWidths=stat_widths)
    stat_grid.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(stat_grid)
    story.append(Spacer(1, 4))

    # Core Strategic Pillars
    story.append(para("Key Strategic Pillars Put in Place", h2_style))
    pillars = [
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
    p_cards = []
    for p_title, p_body, fill in pillars:
        c_table = Table([[para(p_title, card_title_style)], [para(p_body, card_body_style)]], colWidths=[3.42 * inch])
        c_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), fill),
            ('BOX', (0, 0), (-1, -1), 0.35, BORDER),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
            ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        p_cards.append(c_table)

    p_grid = Table([[p_cards[0], p_cards[1]], [p_cards[2], p_cards[3]]], colWidths=[3.48 * inch, 3.48 * inch])
    p_grid.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 1), ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    story.append(p_grid)
    story.append(Spacer(1, 4))
    story.append(para("Detailed breakdown of all completed operational phases and technical deliverables follows on subsequent pages.",
                      ParagraphStyle('Notice', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.8, leading=10, textColor=SAFFRON)))

    # ==================== PAGE 2: TASK BREAKDOWN (PHASES 1 & 2) ====================
    story.append(PageBreak())
    story.append(para("1. Forensic Technical Audit & Catalogue Sanitization (Phase 1)", h2_style))
    story.append(para(
        "Quality Sweets had inherited significant technical legacy debt from older themes (Megnor) and default BigCommerce URL parameters. "
        "We conducted a forensic cleanup to eliminate 404 errors, consolidate redirect chains, and sanitize product naming conventions.",
        body_style))

    t1_headers = ["Workstream", "Specific Tasks & Technical Actions Completed", "Status"]
    t1_widths = [1.5 * inch, 4.6 * inch, 0.85 * inch]
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
    story.append(build_table(t1_headers, t1_rows, t1_widths))
    story.append(Spacer(1, 5))

    story.append(para("2. Conversion Architecture & Content Implementation (Phase 2)", h2_style))
    story.append(para(
        "We built out high-converting dedicated pages to capture different customer intents: nationwide gift buyers, local takeout diners, and corporate/wedding event planners.",
        body_style))

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
    story.append(build_table(["Target Page / Asset", "Implementation & SEO Strategy Delivered", "Status"], t2_rows, t1_widths))

    # ==================== PAGE 3: PHASES 3 & 4 + ROADMAP ====================
    story.append(PageBreak())
    story.append(para("3. Structured Data, Google Profile & Analytics Setup (Phases 3 & 4)", h2_style))

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
    story.append(build_table(["Area", "Configuration & Optimization Delivered", "Status"], t3_rows, t1_widths))
    story.append(Spacer(1, 5))

    story.append(para("Why Commercial Data Starts in Month 2 & Strategic Roadmap", h2_style))
    story.append(para(
        "Sales, revenue, and lead percentage changes are intentionally not included in this first report. "
        "Month 1 was dedicated entirely to building and deploying the technical architecture, indexing the new pages, and establishing clean tracking. "
        "Google requires a full 30-day reporting cycle to crawl, index, and re-rank the sanitized URLs. "
        "Comparing Month 1 against past untracked periods would be statistically misleading; our next report (around November 1, 2026) will provide the first true comparable performance cycle.",
        body_style))

    story.append(para("Month 2 Strategic Roadmap (Upcoming Initiatives):", h3_style))
    rm_items = [
        ("Phase 4.4 — Visual Assets & GBP Posts", "Deploy weekly high-resolution photography of fresh sweets, store displays, and regular Google Business Posts to drive engagement and local relevance."),
        ("Phase 4.5 — Ethical Review Engine", "Implement in-store physical review acceleration (counter QR code cards and packaging inserts) to increase Google review velocity from genuine store visitors."),
        ("Phase 4.6 — Local Citation Authority", "Audit and align NAP consistency across the top 40 local business directories (Yelp, Apple Maps, Bing Places, YellowPages, etc.)."),
        ("Phase 5.1 & 5.2 — Seasonal Landings & GEO", "Deploy evergreen festive campaign landings (Diwali, Holi, Wedding Season) and optimize content for Generative Engine Optimization (ChatGPT, Perplexity, Google AI Overviews).")
    ]
    for title, desc in rm_items:
        story.append(para(f"&bull; <b>{title}:</b> {desc}", bullet_style))

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
        story.append(PageBreak())
        story.append(para(title_text, keyword_title))
        story.append(para(subtitle_text, keyword_subtitle))
        
        img = Image(str(img_path))
        max_w = 6.95 * inch
        max_h = 5.4 * inch
        scale = min(max_w / img.imageWidth, max_h / img.imageHeight)
        img.drawWidth = img.imageWidth * scale
        img.drawHeight = img.imageHeight * scale
        story.append(img)
        story.append(Spacer(1, 4))

        note_table = Table([[para(f"<b>Strategic Analysis & Baseline Context:</b> {notes}", note_body)]], colWidths=[6.95 * inch])
        note_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), GREY),
            ('BOX', (0, 0), (-1, -1), 0.35, BORDER),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(note_table)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter, leftMargin=0.65 * inch, rightMargin=0.65 * inch,
                            topMargin=0.55 * inch, bottomMargin=0.58 * inch,
                            title='Quality Sweets First Month Comprehensive Progress Report')
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Saved expanded PDF: {OUTPUT}")

if __name__ == "__main__":
    build_pdf()
