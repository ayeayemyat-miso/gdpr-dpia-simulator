"""
PDF Generator for DPIA Sign-Off Report
Based on DPC Step 7: Sign off and record outcomes
Source: https://www.dataprotection.ie/en/organisations/know-your-obligations/data-protection-impact-assessments
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os

def generate_dpia_report(session_data, risk_data, signoff_data, filename="dpia_report.pdf"):
    """
    Generate a PDF report of the DPIA process.
    
    Args:
        session_data: Dict from dpia_session.json (Steps 1-2)
        risk_data: List of risks from risk_register.csv (Step 5)
        signoff_data: Dict from Step 7 sign-off form
        filename: Output PDF filename
    """
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=16, spaceAfter=30)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=12, spaceAfter=10, spaceBefore=15)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, spaceAfter=6)
    
    story = []
    
    # Title
    story.append(Paragraph("Data Protection Impact Assessment (DPIA) Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", body_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Based on Irish Data Protection Commission Guidance", body_style))
    story.append(Paragraph("Source: https://www.dataprotection.ie/.../data-protection-impact-assessments", body_style))
    story.append(Spacer(1, 1*cm))
    
    # Step 1: Need Assessment
    story.append(Paragraph("Step 1: Need for DPIA", heading_style))
    if session_data:
        need = session_data.get('need_assessment', {})
        criteria_met = need.get('criteria_met', 0)
        recommendation = need.get('recommendation', 'Not assessed')
        story.append(Paragraph(f"Criteria met: {criteria_met} out of 10", body_style))
        story.append(Paragraph(f"Recommendation: {recommendation}", body_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Step 2: Processing Description
    story.append(Paragraph("Step 2: Description of Processing", heading_style))
    if session_data:
        processing = session_data.get('processing_description', {})
        for key, value in processing.items():
            story.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", body_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Step 5: Risk Register
    story.append(Paragraph("Step 5: Risk Register", heading_style))
    if risk_data:
        for i, risk in enumerate(risk_data, 1):
            story.append(Paragraph(f"<b>Risk {i}:</b> {risk.get('description', 'N/A')}", body_style))
            story.append(Paragraph(f"Likelihood: {risk.get('likelihood', 'N/A')} | Severity: {risk.get('severity', 'N/A')} | Overall: {risk.get('overall_risk', 'N/A')}", body_style))
            story.append(Spacer(1, 0.2*cm))
    else:
        story.append(Paragraph("No risks identified.", body_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Step 7: Sign-Off
    story.append(Paragraph("Step 7: Sign-Off and Outcomes", heading_style))
    if signoff_data:
        story.append(Paragraph(f"<b>Measures approved by:</b> {signoff_data.get('measures_approved_by', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Date:</b> {signoff_data.get('date', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Residual risks approved by:</b> {signoff_data.get('residual_risks_approved_by', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>DPO advice provided:</b> {signoff_data.get('dpo_advice_provided', 'N/A')}", body_style))
        if signoff_data.get('dpo_advice_summary'):
            story.append(Paragraph(f"<b>DPO advice summary:</b> {signoff_data['dpo_advice_summary']}", body_style))
        story.append(Paragraph(f"<b>DPO advice accepted:</b> {signoff_data.get('dpo_advice_accepted', 'N/A')}", body_style))
        if signoff_data.get('overruled_reasons'):
            story.append(Paragraph(f"<b>Reasons for overruling:</b> {signoff_data['overruled_reasons']}", body_style))
        story.append(Paragraph(f"<b>Comments:</b> {signoff_data.get('comments', 'N/A')}", body_style))
    
    # Footer note
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("This report was generated using the DPIA Process Assistant tool.", body_style))
    story.append(Paragraph("It is the responsibility of the Data Controller to ensure full compliance with GDPR.", body_style))
    
    doc.build(story)
    return filename