import os
import datetime
import uuid
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect
from PIL import Image as PILImage

def draw_watermark(canvas, page_width, page_height):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 75)
    canvas.setFillColor(colors.Color(0, 0, 0, alpha=0.04)) 
    canvas.translate(page_width / 2, page_height / 2)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, "MEDIVISION AI")
    canvas.restoreState()

def draw_first_page(canvas, doc):
    """
    Draws the dark blue header block and the background watermark for the first page.
    """
    canvas.saveState()
    page_width, page_height = letter
    header_height = 110
    
    # Draw Header Background
    canvas.setFillColor(colors.HexColor('#1E3A8A')) # Dark Blue
    canvas.rect(0, page_height - header_height, page_width, header_height, fill=1, stroke=0)
    
    # Draw Header Text (Left Side)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 32)
    canvas.drawString(40, page_height - 50, "MediVision AI")
    
    canvas.setFont("Helvetica", 12)
    canvas.drawString(40, page_height - 70, "AI-Powered Chest X-Ray Analysis")
    
    # Draw Header Text (Right Side)
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawRightString(page_width - 40, page_height - 48, "ANALYSIS REPORT")
    
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y | %I:%M:%S %p")
    canvas.setFont("Helvetica", 11)
    canvas.drawRightString(page_width - 40, page_height - 70, timestamp)
    
    canvas.restoreState()
    
    # Draw Watermark
    draw_watermark(canvas, page_width, page_height)


def draw_later_pages(canvas, doc):
    """
    Draws only the watermark for subsequent pages (no header).
    """
    page_width, page_height = letter
    draw_watermark(canvas, page_width, page_height)


def generate_pdf_report(image_file, predicted_class, confidence, probabilities, inference_time):
    buffer = BytesIO()
    
    # Top margin accommodates the header on the first page
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=130, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    styles.add(ParagraphStyle(name='Heading2Style', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#1E293B'), spaceAfter=10))
    styles.add(ParagraphStyle(name='NormalStyle', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#334155'), leading=14))
    styles.add(ParagraphStyle(name='DisclaimerStyle', fontName='Helvetica-Oblique', fontSize=9, textColor=colors.HexColor('#64748B'), alignment=1))
    styles.add(ParagraphStyle(name='SignatureStyle', fontName='Helvetica-Oblique', fontSize=12, textColor=colors.HexColor('#1E3A8A'), spaceAfter=2))
    
    if predicted_class == "COVID":
        pred_color = colors.HexColor('#EF4444')
    elif predicted_class == "Viral Pneumonia":
        pred_color = colors.HexColor('#F59E0B')
    else:
        pred_color = colors.HexColor('#10B981')
        
    Story = []
    
    patient_id = f"PT-{str(uuid.uuid4())[:8].upper()}"
    analysis_id = f"ANX-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
    
    info_data = [
        ["Patient ID:", patient_id, "Analysis ID:", analysis_id],
        ["Model:", "EfficientNetB0", "Resolution:", "224x224"]
    ]
    info_table = Table(info_data, colWidths=[80, 175, 80, 175])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#334155')),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.lightgrey),
    ]))
    Story.append(info_table)
    Story.append(Spacer(1, 15))
    
    Story.append(Paragraph("Input X-Ray Image", styles['Heading2Style']))
    img_temp_path = "temp_report_img.png"
    img = PILImage.open(image_file)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    aspect = img.width / float(img.height)
    pdf_img_width = 230
    pdf_img_height = pdf_img_width / aspect
    
    img.save(img_temp_path)
    report_img = Image(img_temp_path, width=pdf_img_width, height=pdf_img_height)
    report_img.hAlign = 'CENTER'
    Story.append(report_img)
    Story.append(Spacer(1, 15))
    
    Story.append(Paragraph("AI Inference Results", styles['Heading2Style']))
    
    res_data = [
        ["Primary Prediction", "Confidence Score", "Inference Time"],
        [predicted_class, f"{confidence:.2f}%", f"{inference_time*1000:.1f} ms"]
    ]
    
    res_table = Table(res_data, colWidths=[170, 170, 170])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#475569')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('TEXTCOLOR', (0, 1), (0, 1), pred_color),
        ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (0, 1), 14),
        ('FONTSIZE', (1, 1), (-1, 1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 12),
        ('TOPPADDING', (0, 1), (-1, 1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    Story.append(res_table)
    Story.append(Spacer(1, 15))
    
    Story.append(Paragraph("Confidence Level", styles['NormalStyle']))
    Story.append(Spacer(1, 5))
    
    d = Drawing(500, 20)
    d.add(Rect(0, 0, 500, 15, fillColor=colors.HexColor('#E2E8F0'), strokeColor=None, rx=5, ry=5))
    fill_width = max(10, (confidence / 100.0) * 500)
    d.add(Rect(0, 0, fill_width, 15, fillColor=pred_color, strokeColor=None, rx=5, ry=5))
    
    Story.append(d)
    Story.append(Spacer(1, 15))
    
    # ---------------------------------------------------------
    # Use KeepTogether so the Probability Table doesn't split
    # ---------------------------------------------------------
    prob_elements = []
    prob_elements.append(Paragraph("Class Probabilities Breakdown", styles['Heading2Style']))
    
    classes = ['COVID', 'Normal', 'Viral Pneumonia']
    prob_data = [["Condition", "Probability"]]
    for cls, prob in zip(classes, probabilities):
        prob_data.append([cls, f"{prob * 100:.2f}%"])
        
    prob_table = Table(prob_data, colWidths=[255, 255])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')), 
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    prob_elements.append(prob_table)
    prob_elements.append(Spacer(1, 15))
    
    Story.append(KeepTogether(prob_elements))
    
    # Detailed Explanation
    explanation = f"""This report was generated by MediVision AI using the EfficientNetB0 deep learning architecture. 
    The model analyzed the provided frontal chest X-ray and predicted the class <b>{predicted_class}</b> with a confidence 
    score of <b>{confidence:.2f}%</b>. This score represents the mathematical probability assigned by the neural network 
    based on learned patterns from its training dataset. It is not equivalent to a definitive medical diagnosis."""
    Story.append(Paragraph(explanation, styles['NormalStyle']))
    Story.append(Spacer(1, 20))
    
    # ---------------------------------------------------------
    # Digital Signature Section
    # ---------------------------------------------------------
    sig_elements = []
    sig_elements.append(Paragraph("Digitally Signed by:", styles['NormalStyle']))
    sig_elements.append(Spacer(1, 5))
    sig_elements.append(Paragraph("MediVision AI Automated System", styles['SignatureStyle']))
    sig_elements.append(Paragraph(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['NormalStyle']))
    sig_elements.append(Paragraph(f"Analysis ID: {analysis_id}", styles['NormalStyle']))
    sig_elements.append(Spacer(1, 30))
    
    Story.append(KeepTogether(sig_elements))
    
    # Footer Disclaimer
    disclaimer = """<b>MEDICAL DISCLAIMER:</b> This AI prediction is intended exclusively for educational and research 
    purposes. It is not a medical diagnostic tool, FDA approved, or intended to replace professional evaluation, 
    diagnosis, or treatment by a qualified healthcare provider."""
    Story.append(Paragraph(disclaimer, styles['DisclaimerStyle']))
    
    # Pass different drawing functions for first vs later pages
    doc.build(Story, onFirstPage=draw_first_page, onLaterPages=draw_later_pages)
    
    if os.path.exists(img_temp_path):
        os.remove(img_temp_path)
        
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
