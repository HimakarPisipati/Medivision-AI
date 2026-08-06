import os
import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from PIL import Image as PILImage

def generate_pdf_report(image_file, predicted_class, confidence, probabilities, inference_time):
    """
    Generates a professional PDF report.
    Returns the PDF bytes.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))
    
    Story = []
    
    # Title
    Story.append(Paragraph("<b>MediVision AI</b> - Patient X-Ray Report", styles['Title']))
    Story.append(Spacer(1, 12))
    
    # Timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Story.append(Paragraph(f"<b>Date & Time:</b> {timestamp}", styles['Normal']))
    Story.append(Spacer(1, 12))
    
    # Image
    # Save the uploaded file temporarily or read from buffer to pass to reportlab Image
    img_temp_path = "temp_report_img.png"
    img = PILImage.open(image_file)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save(img_temp_path)
    
    report_img = Image(img_temp_path, width=250, height=250)
    Story.append(report_img)
    Story.append(Spacer(1, 24))
    
    # Prediction Results
    Story.append(Paragraph("<b>Prediction Results</b>", styles['Heading2']))
    Story.append(Spacer(1, 12))
    
    data = [
        ["Metric", "Value"],
        ["Prediction", predicted_class],
        ["Confidence", f"{confidence:.2f}%"],
        ["Model", "EfficientNetB0 (Transfer Learning)"],
        ["Inference Time", f"{inference_time:.4f} seconds"]
    ]
    
    table = Table(data, colWidths=[150, 250])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    Story.append(table)
    Story.append(Spacer(1, 24))
    
    # Probabilities
    Story.append(Paragraph("<b>Class Probabilities</b>", styles['Heading2']))
    Story.append(Spacer(1, 12))
    
    classes = ['COVID', 'Normal', 'Viral Pneumonia']
    prob_data = [["Class", "Probability"]]
    for cls, prob in zip(classes, probabilities):
        prob_data.append([cls, f"{prob * 100:.2f}%"])
        
    prob_table = Table(prob_data, colWidths=[150, 250])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.aliceblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    Story.append(prob_table)
    Story.append(Spacer(1, 48))
    
    # Disclaimer
    disclaimer = ("<font size=8 color=gray><b>Medical Disclaimer:</b> This AI prediction is intended only for "
                  "educational and research purposes. It should not replace professional medical diagnosis.</font>")
    Story.append(Paragraph(disclaimer, styles['Normal']))
    
    doc.build(Story)
    
    # Clean up temp image
    if os.path.exists(img_temp_path):
        os.remove(img_temp_path)
        
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
