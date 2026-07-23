from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from typing import Dict, Any, List


def create_pdf_report(
    title: str,
    content: Dict[str, Any],
    data: List[Dict[str, Any]] = None
) -> BytesIO:
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    
    elements = []
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 12))
    
    for key, value in content.items():
        elements.append(Paragraph(f"<b>{key}:</b> {value}", styles['Normal']))
        elements.append(Spacer(1, 6))
    
    if data:
        elements.append(Spacer(1, 20))
        headers = list(data[0].keys()) if data else []
        table_data = [headers]
        for row in data:
            table_data.append([str(row.get(h, '')) for h in headers])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
    
    doc.build(elements)
    output.seek(0)
    return output
