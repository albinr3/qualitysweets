from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.pdfbase.pdfmetrics import stringWidth
from pathlib import Path

OUTPUT = Path('outputs/pdf/Quality_Sweets_First_Month_Progress_Report_September_2026.pdf')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = letter
NAVY = colors.HexColor('#24323D')
SAFFRON = colors.HexColor('#C9851C')
GOLD = colors.HexColor('#F8F0DE')
BLUE = colors.HexColor('#EDF3F6')
GREEN = colors.HexColor('#EAF3EC')
GREY = colors.HexColor('#F3F4F6')
MID = colors.HexColor('#6B7280')
DARK = colors.HexColor('#2F3A42')
BORDER = colors.HexColor('#D9D9D9')


def p(text, style):
    return Paragraph(text, style)


styles = getSampleStyleSheet()
title = ParagraphStyle('Title', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=23,
                       leading=25, textColor=colors.black, spaceAfter=1)
subtitle = ParagraphStyle('Subtitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5,
                          leading=13, textColor=SAFFRON, spaceAfter=7)
intro = ParagraphStyle('Intro', parent=styles['Normal'], fontName='Helvetica', fontSize=10.05,
                       leading=13.1, textColor=DARK, spaceAfter=5)
h2 = ParagraphStyle('H2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13,
                    leading=16, textColor=colors.black, spaceBefore=7, spaceAfter=5)
card_title = ParagraphStyle('CardTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.6,
                            leading=11.5, textColor=NAVY, spaceAfter=2)
card_body = ParagraphStyle('CardBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8.4,
                           leading=10.2, textColor=colors.HexColor('#374151'))
timeline_title = ParagraphStyle('TimelineTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.4,
                                leading=11.2, textColor=colors.black, spaceAfter=1)
timeline_body = ParagraphStyle('TimelineBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8.35,
                               leading=10.2, textColor=colors.HexColor('#374151'))
date_style = ParagraphStyle('Date', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.3,
                            leading=10, textColor=NAVY, alignment=TA_CENTER)
table_head = ParagraphStyle('TableHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.25,
                            leading=9.4, textColor=colors.white)
table_left = ParagraphStyle('TableLeft', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.6,
                            leading=10.2, textColor=NAVY)
table_body = ParagraphStyle('TableBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8.25,
                            leading=10.0, textColor=colors.HexColor('#374151'))
status = ParagraphStyle('Status', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.9,
                        leading=9.2, textColor=NAVY, alignment=TA_CENTER)
small = ParagraphStyle('Small', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5,
                       leading=10.7, textColor=MID)
body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=9.7,
                      leading=12.1, textColor=DARK)
bullet = ParagraphStyle('Bullet', parent=styles['Normal'], fontName='Helvetica', fontSize=9.0,
                        leading=11.8, textColor=DARK, leftIndent=14, firstLineIndent=-9, spaceAfter=2)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 7.4)
    canvas.setFillColor(MID)
    canvas.drawRightString(PAGE_W - 0.65*inch, PAGE_H - 0.36*inch, 'QUALITY SWEETS  |  FIRST MONTH UPDATE')
    canvas.setFont('Helvetica', 7.2)
    canvas.drawCentredString(PAGE_W / 2, 0.33*inch, 'Quality Sweets  |  First Month Progress Report')
    canvas.restoreState()


story = []
story.append(p('First Month Progress Report', title))
story.append(p(
    'This first month focused on building a stronger online foundation for Quality Sweets. '
    'The work completed makes it easier for customers to find the business, understand the offer, and take the next step online. '
    'The goal was to put the right systems in place before measuring commercial performance.', intro))

story.append(p('What we put in place', h2))
cards = [
    [p('Clearer website journey', card_title), p('A simpler path from the homepage to sweets, takeout, local pickup and catering.', card_body)],
    [p('Cleaner product catalogue', card_title), p('Product names, page addresses and old links were cleaned up to reduce confusion.', card_body)],
    [p('Stronger local presence', card_title), p('The Google Business Profile now reflects the store, takeout service and key offerings more clearly.', card_body)],
    [p('Ready to measure progress', card_title), p('Tracking is in place so upcoming reports can focus on meaningful customer actions.', card_body)],
]
card_grid = Table([[cards[0], cards[1]], [cards[2], cards[3]]], colWidths=[3.45*inch, 3.45*inch])
card_grid.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), GOLD), ('BACKGROUND', (1,0), (1,0), BLUE),
    ('BACKGROUND', (0,1), (0,1), GREEN), ('BACKGROUND', (1,1), (1,1), GREY),
    ('BOX', (0,0), (-1,-1), 0.35, BORDER), ('INNERGRID', (0,0), (-1,-1), 0.35, BORDER),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('LEFTPADDING', (0,0), (-1,-1), 9),
    ('RIGHTPADDING', (0,0), (-1,-1), 9), ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
]))
story.append(card_grid)

story.append(p('Work completed', h2))
timeline_rows = [
    ('Website and online ordering', 'Website and online ordering foundation',
     'Improved the main website structure; created clearer pages for takeout, the Iselin store and catering; refreshed the homepage; and added helpful content to the main sweets and gift categories.', GOLD),
    ('Product catalogue', 'Cleaner catalogue and easier navigation',
     'Updated category page addresses, cleaned eight pickup-only product pages, and made sure older links lead customers to the right current pages.', BLUE),
    ('Local business profile', 'Local business information and menu',
     'Aligned the store details used online, clarified that service is takeout and pickup only, and updated the Google Business Profile with products and menu information.', GREEN),
    ('Measurement setup', 'Measurement setup',
     'Added tracking for purchases, catering inquiries, calls, emails, directions and menu visits. This creates a reliable starting point for future reports.', GREY),
    ('Google Shopping', 'More product visibility on Google',
     'Connected the online catalogue to Google Shopping free listings so eligible sweets, snacks and gift boxes can be discovered in Google.', GOLD),
]
timeline_data = []
for d, t, b, fill in timeline_rows:
    timeline_data.append([p(d, date_style), [p(t, timeline_title), p(b, timeline_body)]])
timeline = Table(timeline_data, colWidths=[1.8*inch, 5.1*inch], rowHeights=[0.62*inch]*5)
commands = [
    ('BOX', (0,0), (-1,-1), 0.35, BORDER), ('INNERGRID', (0,0), (-1,-1), 0.35, BORDER),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('LEFTPADDING', (0,0), (-1,-1), 7),
    ('RIGHTPADDING', (0,0), (-1,-1), 7), ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]
for idx, (_,_,_,fill) in enumerate(timeline_rows):
    commands.append(('BACKGROUND', (0,idx), (0,idx), fill))
timeline.setStyle(TableStyle(commands))
story.append(timeline)
story.append(Spacer(1, 6))
story.append(p('This is a foundation report. Commercial changes need a full period of customer activity after the new website, local profile and tracking improvements are in place.', small))

story.append(PageBreak())
story.append(p('Google Maps visibility baseline', h2))
story.append(p('The grid checks below are the starting point for tracking local visibility. Green means the business is already appearing near the top of the map grid; amber and red show where there is room to improve.', body))
story.append(Spacer(1, 5))

map_headers = [p('Tracked search', table_head), p('Current grid snapshot', table_head), p('What it tells us', table_head)]
map_rows = [
    ('Indian sweets shop near me', 'Strong visibility\nMostly positions 1-5', 'A strong starting position for a core local search.', GREEN),
    ('Bengali sweets', 'Very strong visibility\nMostly positions 1-2', 'Quality Sweets is highly visible for this specialty.', GREEN),
    ('Indian sweets near me', 'Mixed visibility\nPositions 4 to 20+', 'A priority opportunity to expand local reach.', GOLD),
    ('Samosas near me', 'Limited visibility\nMostly 20+', 'An area to build through the takeout menu and local content.', colors.HexColor('#FCE8E6')),
    ('Samosa chaat near me', 'Limited visibility\nMostly 20+', 'An area to build through the takeout menu and local content.', colors.HexColor('#FCE8E6')),
    ('Chaat near me', 'Limited visibility\nMostly 20+', 'An area to build through the takeout menu and local content.', colors.HexColor('#FCE8E6')),
    ('Pani puri near me', 'Limited visibility\nMostly 20+', 'An area to build through the takeout menu and local content.', colors.HexColor('#FCE8E6')),
]
map_data = [map_headers]
for keyword, snapshot, takeaway, fill in map_rows:
    map_data.append([p(keyword, table_left), p(snapshot.replace('\n', '<br/>'), status), p(takeaway, table_body)])
map_table = Table(map_data, colWidths=[2.05*inch, 1.75*inch, 3.1*inch], rowHeights=[0.34*inch]+[0.46*inch]*7)
map_cmd = [
    ('BACKGROUND', (0,0), (-1,0), NAVY), ('BOX', (0,0), (-1,-1), 0.35, BORDER),
    ('INNERGRID', (0,0), (-1,-1), 0.35, BORDER), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 7), ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]
for row_no, (_,_,_,fill) in enumerate(map_rows, start=1):
    map_cmd.append(('BACKGROUND', (1,row_no), (1,row_no), fill))
map_table.setStyle(TableStyle(map_cmd))
story.append(map_table)

story.append(p('Why there are no commercial changes in this report', h2))
story.append(p('This first report does not include sales, revenue or lead changes because the period was used to repair and prepare the online foundation. The improvements need time for Google to process them and for customers to interact with the updated website and local profile. The Maps grid above is a visibility baseline, not a commercial result.', body))

story.append(p('What happens next', h2))
for item in [
    'Add the website information Google needs to better understand the business, products and pages.',
    'Build local trust with real photos, regular Google updates and a simple review request process.',
    'Monitor customer actions and use the data to guide the next priorities.'
]:
    story.append(p('&bull; ' + item, bullet))
story.append(Spacer(1, 3))
story.append(p('<b>Next report:</b> expected around November 1, 2026. It will include the first comparable visibility and customer-action results.', body))

doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter, leftMargin=0.65*inch, rightMargin=0.65*inch,
                        topMargin=0.55*inch, bottomMargin=0.58*inch, title='Quality Sweets First Month Progress Report')
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUTPUT)
