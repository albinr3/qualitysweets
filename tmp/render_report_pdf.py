import pypdfium2 as pdfium
from pathlib import Path

src = Path('outputs/pdf/Quality_Sweets_First_Month_Progress_Report_September_2026.pdf')
out = Path('tmp/first_month_report_pdf_render')
out.mkdir(parents=True, exist_ok=True)
pdf = pdfium.PdfDocument(src)
for i in range(len(pdf)):
    page = pdf[i]
    image = page.render(scale=2.0).to_pil()
    image.save(out / f'page-{i+1}.png')
print(f'pages={len(pdf)} output={out}')
