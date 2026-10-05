from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
)

OUTPUT = Path('outputs/pdf/Quality_Sweets_First_Month_Progress_Report_September_2026.pdf')
BASELINE = Path('baseline')
HEATMAP = Path(r'C:\Users\Albin Rodriguez\Downloads\Mapa de calor SEO en Nueva Jersey.png')

NAVY = colors.HexColor('#24323D')
SAFFRON = colors.HexColor('#C9851C')
GOLD = colors.HexColor('#F8F0DE')
BLUE = colors.HexColor('#EDF3F6')
GREEN = colors.HexColor('#EAF3EC')
GREY = colors.HexColor('#F3F4F6')
MID = colors.HexColor('#6B7280')
DARK = colors.HexColor('#2F3A42')
BORDER = colors.HexColor('#D9D9D9')
PAGE_W, PAGE_H = letter


def para(text, style):
    return Paragraph(text, style)


styles = getSampleStyleSheet()
title = ParagraphStyle('Title', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=23,
                       leading=26, textColor=colors.black, spaceAfter=5)
intro = ParagraphStyle('Intro', parent=styles['Normal'], fontName='Helvetica', fontSize=10.2,
                       leading=13.2, textColor=DARK, spaceAfter=6)
h2 = ParagraphStyle('H2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13,
                    leading=16, textColor=colors.black, spaceBefore=8, spaceAfter=5)
card_title = ParagraphStyle('CardTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.8,
                            leading=11.5, textColor=NAVY, spaceAfter=2)
card_body = ParagraphStyle('CardBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8.55,
                           leading=10.4, textColor=colors.HexColor('#374151'))
area = ParagraphStyle('Area', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.0,
                      leading=11, textColor=NAVY, alignment=TA_CENTER)
work_title = ParagraphStyle('WorkTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5,
                            leading=11, textColor=colors.black, spaceAfter=1)
work_body = ParagraphStyle('WorkBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5,
                           leading=10.25, textColor=colors.HexColor('#374151'))
small = ParagraphStyle('Small', parent=styles['Normal'], fontName='Helvetica', fontSize=8.7,
                       leading=11, textColor=MID)
body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=10.1,
                      leading=13, textColor=DARK)
bullet = ParagraphStyle('Bullet', parent=styles['Normal'], fontName='Helvetica', fontSize=9.3,
                        leading=12.1, textColor=DARK, leftIndent=14, firstLineIndent=-9, spaceAfter=3)
image_caption = ParagraphStyle('ImageCaption', parent=styles['Normal'], fontName='Helvetica', fontSize=8.2,
                               leading=10, textColor=MID, alignment=TA_CENTER, spaceBefore=5)
keyword_title = ParagraphStyle('KeywordTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=18,
                               leading=22, textColor=colors.black, alignment=TA_CENTER, spaceAfter=9)
keyword_subtitle = ParagraphStyle('KeywordSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=9,
                                  leading=11, textColor=MID, alignment=TA_CENTER, spaceAfter=10)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MID)
    canvas.setFont('Helvetica-Bold', 7.4)
    canvas.drawRightString(PAGE_W - 0.65 * inch, PAGE_H - 0.36 * inch, 'QUALITY SWEETS  |  FIRST MONTH UPDATE')
    canvas.setFont('Helvetica', 7.2)
    canvas.drawCentredString(PAGE_W / 2, 0.33 * inch, 'Quality Sweets  |  First Month Progress Report')
    canvas.restoreState()


def card(title_text, body_text, fill):
    table = Table([[[para(title_text, card_title), para(body_text, card_body)]]], colWidths=[3.45 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), fill),
        ('BOX', (0, 0), (-1, -1), 0.35, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 9), ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return table


def image_page(title_text, image_path, caption):
    subtitle_text = 'New Jersey local search scan' if title_text == 'New Jersey SEO Heat Map' else 'Google Maps grid scan'
    flow = [PageBreak(), para(title_text, keyword_title), para(subtitle_text, keyword_subtitle)]
    img = Image(str(image_path))
    max_w = 7.05 * inch
    max_h = 5.65 * inch
    scale = min(max_w / img.imageWidth, max_h / img.imageHeight)
    img.drawWidth = img.imageWidth * scale
    img.drawHeight = img.imageHeight * scale
    flow.extend([img, para(caption, image_caption)])
    return flow


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
story = []

# Page 1
story.append(para('First Month Progress Report', title))
story.append(para(
    'This report records the work completed during the first month: website updates, a clearer product catalogue, local business information, and tracking for customer actions.',
    intro))
story.append(para('What we put in place', h2))
cards = [
    card('Clearer website journey', 'A simpler path from the homepage to sweets, takeout, local pickup and catering.', GOLD),
    card('Cleaner product catalogue', 'Product names, page addresses and old links were cleaned up to reduce confusion.', BLUE),
    card('Stronger local presence', 'The Google Business Profile now reflects the store, takeout service and key offerings more clearly.', GREEN),
    card('Ready to measure activity', 'Tracking is in place for customer actions such as calls, directions, menu visits and inquiries.', GREY),
]
grid = Table([[cards[0], cards[1]], [cards[2], cards[3]]], colWidths=[3.45 * inch, 3.45 * inch])
grid.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
story.append(grid)
story.append(para('Work completed', h2))
work = [
    ('Website and online ordering', 'Clearer pages for customers', 'Improved the website structure; created clearer pages for takeout, the Iselin store and catering; refreshed the homepage; and added useful information to the main sweets and gift categories.', GOLD),
    ('Product catalogue', 'Cleaner catalogue and easier navigation', 'Updated category page addresses, cleaned eight pickup-only product pages, and made sure older links lead customers to the current pages.', BLUE),
    ('Local business profile', 'Store details, products and menu', 'Aligned the store details used online, clarified takeout and pickup service, and updated the Google Business Profile with products and menu information.', GREEN),
    ('Measurement', 'Customer-action tracking', 'Added tracking for purchases, catering inquiries, calls, emails, directions and menu visits.', GREY),
    ('Google Shopping', 'More product visibility on Google', 'Connected eligible sweets, snacks and gift boxes to Google Shopping free listings.', GOLD),
]
work_data = []
for area_text, title_text, body_text, fill in work:
    work_data.append([para(area_text, area), [para(title_text, work_title), para(body_text, work_body)]])
work_table = Table(work_data, colWidths=[1.8 * inch, 5.1 * inch], rowHeights=[0.62 * inch] * len(work))
commands = [
    ('BOX', (0, 0), (-1, -1), 0.35, BORDER), ('INNERGRID', (0, 0), (-1, -1), 0.35, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (-1, -1), 7),
    ('RIGHTPADDING', (0, 0), (-1, -1), 7), ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]
for i, (_, _, _, fill) in enumerate(work):
    commands.append(('BACKGROUND', (0, i), (0, i), fill))
work_table.setStyle(TableStyle(commands))
story.append(work_table)
story.append(Spacer(1, 7))
story.append(para('The next report is expected around November 1, 2026. It will compare the first full cycle of visibility and customer-action data.', small))

# Page 2
story.append(PageBreak())
story.append(para('Google Maps starting point', h2))
story.append(para(
    'The following grid scans record current Google Maps positions for the tracked searches. They provide a starting reference for later reports.',
    body))
story.append(para('Why this report does not include commercial changes', h2))
story.append(para(
    'Sales, revenue and lead changes are not included because this period was used to prepare the website, Google Business Profile and tracking. The updated pages and listing need a full reporting cycle before customer activity can be compared. The grid scans show local visibility, not sales results.',
    body))
story.append(para('What happens next', h2))
for item in [
    'Add the website information Google needs to better understand the business, products and pages.',
    'Add real photos, regular Google updates and a simple review request process.',
    'Review customer actions and use the data to guide the next priorities.'
]:
    story.append(para('&bull; ' + item, bullet))
story.append(Spacer(1, 8))
story.append(para('The grid scans and New Jersey heat map follow. Each image is included in its original form.', small))

screens = [
    ('Indian sweets shop near me', BASELINE / 'Captura de pantalla 2026-10-03 163017.png'),
    ('Indian sweets near me', BASELINE / 'Captura de pantalla 2026-10-03 163116.png'),
    ('Samosas near me', BASELINE / 'Captura de pantalla 2026-10-03 163149.png'),
    ('Samosa chaat near me', BASELINE / 'Captura de pantalla 2026-10-03 163212.png'),
    ('Chaat near me', BASELINE / 'Captura de pantalla 2026-10-03 163257.png'),
    ('Bengali sweets', BASELINE / 'Captura de pantalla 2026-10-03 163320.png'),
    ('Pani puri near me', BASELINE / 'Captura de pantalla 2026-10-03 163354.png'),
]
for keyword, path in screens:
    story.extend(image_page(keyword, path, 'Original Google Maps grid scan for this tracked search.'))

story.extend(image_page('New Jersey SEO Heat Map', HEATMAP, 'Original New Jersey SEO heat map.'))

doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter, leftMargin=0.65 * inch, rightMargin=0.65 * inch,
                        topMargin=0.55 * inch, bottomMargin=0.58 * inch,
                        title='Quality Sweets First Month Progress Report')
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUTPUT)
