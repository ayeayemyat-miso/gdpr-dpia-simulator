"""
Step 4: Sign off and record outcomes
Based on DPC Sample DPIA Template Step 7
"""

import streamlit as st
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER

st.set_page_config(page_title="Step 4: Report & Sign-Off", page_icon="📄")

st.title("📄 Step 4: Report & Sign-Off")
st.caption("Based on DPC Sample DPIA Template - Step 7: Sign off and record outcomes")

# Generate PDF function
def generate_dpia_report(session_data, official_data, risk_data, signoff_data, filename):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=16, spaceAfter=30)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=12, spaceAfter=10, spaceBefore=15)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, spaceAfter=6)
    
    story = []
    
    story.append(Paragraph("Data Protection Impact Assessment (DPIA) Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", body_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Based on Irish Data Protection Commission Guidance", body_style))
    story.append(Spacer(1, 1*cm))
    
    # Official Irish List
    story.append(Paragraph("Official Irish DPIA List (Article 35(4))", heading_style))
    if official_data:
        story.append(Paragraph(f"Criteria met: {official_data.get('criteria_met', 0)} out of 10", body_style))
        story.append(Paragraph(f"DPIA Required by Irish Law: {'Yes' if official_data.get('requires_dpia', False) else 'No'}", body_style))
    else:
        story.append(Paragraph("Official Irish List assessment not completed.", body_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Step 1: WP29 Criteria
    story.append(Paragraph("WP29 Risk Criteria Assessment", heading_style))
    if session_data.get('need_assessment'):
        need = session_data['need_assessment']
        story.append(Paragraph(f"Criteria met: {need.get('criteria_met', 0)} out of 9", body_style))
        story.append(Paragraph(f"Recommendation: {need.get('recommendation', 'Not assessed')}", body_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Step 2: Processing Description
    story.append(Paragraph("Description of Processing", heading_style))
    if session_data.get('processing_description'):
        processing = session_data['processing_description']
        for key, value in processing.items():
            if key != "last_updated" and value:
                story.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {str(value)[:200]}", body_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Step 3: Risk Register
    story.append(Paragraph("Risk Register", heading_style))
    if risk_data:
        high_count = len([r for r in risk_data if r.get('overall_risk') == 'High'])
        medium_count = len([r for r in risk_data if r.get('overall_risk') == 'Medium'])
        low_count = len([r for r in risk_data if r.get('overall_risk') == 'Low'])
        story.append(Paragraph(f"Risk Summary: High: {high_count} | Medium: {medium_count} | Low: {low_count}", body_style))
        story.append(Spacer(1, 0.2*cm))
        for i, risk in enumerate(risk_data, 1):
            story.append(Paragraph(f"<b>Risk {i}:</b> {risk.get('description', 'N/A')}", body_style))
            story.append(Paragraph(f"Likelihood: {risk.get('likelihood', 'N/A')} | Severity: {risk.get('severity', 'N/A')} | Overall: {risk.get('overall_risk', 'N/A')}", body_style))
            if risk.get('mitigation'):
                story.append(Paragraph(f"Mitigation: {risk['mitigation'][:150]}", body_style))
            story.append(Spacer(1, 0.2*cm))
    else:
        story.append(Paragraph("No risks identified.", body_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Step 4: Sign-Off
    story.append(Paragraph("Sign-Off and Outcomes", heading_style))
    if signoff_data:
        story.append(Paragraph(f"<b>Measures approved by:</b> {signoff_data.get('measures_approved_by', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Date:</b> {signoff_data.get('date', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Residual risks approved by:</b> {signoff_data.get('residual_risks_approved_by', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>DPO advice provided:</b> {signoff_data.get('dpo_advice_provided', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>DPO advice accepted:</b> {signoff_data.get('dpo_advice_accepted', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Consultation reviewed by:</b> {signoff_data.get('consultation_reviewed_by', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Comments:</b> {signoff_data.get('comments', 'N/A')}", body_style))
    
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("This report was generated using the DPIA Process Assistant tool.", body_style))
    story.append(Paragraph("It is the responsibility of the Data Controller to ensure full compliance with GDPR.", body_style))
    
    doc.build(story)
    return filename

# Check if previous steps have data
has_need_assessment = 'need_assessment' in st.session_state
has_official_list = 'official_dpia_assessment' in st.session_state
has_processing = 'processing_description' in st.session_state
has_risks = len(st.session_state.get('risk_register', [])) > 0

if not has_need_assessment:
    st.warning("⚠️ Please complete Step 1 (WP29 Criteria) first.")
    st.stop()

# --- NEW: High Risk Warning Banner ---
high_risk_count = len([r for r in st.session_state.get('risk_register', []) if r.get('overall_risk') == 'High'])

if high_risk_count > 0:
    st.error(f"""
    ⚠️ **{high_risk_count} High Risk(s) Identified**
    
    **DPO consultation is mandatory** under GDPR Article 35(2). 
    **DPC consultation may be required** under GDPR Article 36 if residual high risks remain after mitigation.
    """)
else:
    st.success("✅ No high risks identified. Standard sign-off procedure is acceptable.")

# Display summary of previous steps
with st.expander("⚖️ Official Irish DPIA List Summary", expanded=False):
    if has_official_list:
        official = st.session_state.official_dpia_assessment
        st.write(f"**Official criteria met:** {official.get('criteria_met', 0)} / 10")
        st.write(f"**Conclusion:** {'DPIA Required by Irish Law' if official.get('requires_dpia', False) else 'Not on Official List'}")
        if official.get('requires_dpia', False):
            st.warning("⚠️ This processing operation matches the official Irish DPC list and **requires a DPIA by law**.")
    else:
        st.info("Official Irish DPIA List not yet completed. Please complete it from the sidebar for full compliance assessment.")

with st.expander("📋 Step 1 Summary: WP29 Criteria", expanded=False):
    need = st.session_state.need_assessment
    st.write(f"**Criteria met:** {need.get('criteria_met', 0)} / 9")
    st.write(f"**Recommendation:** {need.get('recommendation', 'N/A')}")

with st.expander("📝 Step 2 Summary: Processing Description", expanded=False):
    if has_processing:
        processing = st.session_state.processing_description
        for key, value in processing.items():
            if key != "last_updated" and value:
                display_value = str(value)[:200] + "..." if len(str(value)) > 200 else value
                st.write(f"**{key.replace('_', ' ').title()}:** {display_value}")
    else:
        st.info("Step 2 not completed yet. Complete it to include in final report.")

with st.expander("⚠️ Step 3 Summary: Risk Register", expanded=False):
    if has_risks:
        total_risks = len(st.session_state.risk_register)
        high_risks = len([r for r in st.session_state.risk_register if r.get('overall_risk') == 'High'])
        medium_risks = len([r for r in st.session_state.risk_register if r.get('overall_risk') == 'Medium'])
        low_risks = len([r for r in st.session_state.risk_register if r.get('overall_risk') == 'Low'])
        st.write(f"**Total risks identified:** {total_risks}")
        st.write(f"**High risks:** {high_risks} | **Medium:** {medium_risks} | **Low:** {low_risks}")
        
        # Display risks table
        if total_risks > 0:
            st.markdown("#### Risk Details")
            for risk in st.session_state.risk_register:
                st.markdown(f"""
                - **{risk.get('description', 'N/A')}**  
                  Likelihood: {risk.get('likelihood', 'N/A')} | Severity: {risk.get('severity', 'N/A')} | Overall: {risk.get('overall_risk', 'N/A')}
                """)
    else:
        st.info("No risks added yet. Add risks to complete the DPIA process.")

# DPC Consultation Warning
st.warning("""
⚠️ **Important - GDPR Article 36 Requirement**

If, after implementing all mitigation measures, any **high risks remain unresolved**, you must **consult the Data Protection Commission (DPC)** before proceeding with the processing.
""")

# Sign-Off Form
st.markdown("### ✍️ Sign-Off and Outcomes")
st.markdown("Complete this section to finalize the DPIA process.")

with st.form("signoff_form"):
    st.markdown("#### Measures Approval")
    
    col1, col2 = st.columns(2)
    with col1:
        measures_approved_by = st.text_input(
            "Measures approved by (name)", 
            placeholder="Full name",
            help="Authorised signatory with budget authority for implementing measures"
        )
    with col2:
        signoff_date = st.date_input("Date", datetime.now())
    
    st.markdown("#### Residual Risks")
    residual_approved_by = st.text_input(
        "Residual risks approved by (name)", 
        placeholder="Full name",
        help="Senior management or DPO who accepts remaining risks"
    )
    
    st.markdown("#### DPO Advice")
    dpo_advice_provided = st.radio("Was DPO advice provided?", ["No", "Yes"])
    dpo_advice_summary = ""
    if dpo_advice_provided == "Yes":
        dpo_advice_summary = st.text_area(
            "Summary of DPO advice", 
            placeholder="What did the DPO recommend?"
        )
    
    dpo_advice_accepted = st.radio(
        "Was DPO advice accepted?", 
        ["Yes - accepted", "No - overruled"], 
        disabled=(dpo_advice_provided == "No")
    )
    overruled_reasons = ""
    if dpo_advice_accepted == "No - overruled":
        overruled_reasons = st.text_area(
            "Reasons for overruling", 
            placeholder="Explain why DPO advice was not accepted (documentation required for audit trail)"
        )
    
    st.markdown("#### Consultation")
    consultation_reviewed_by = st.text_input(
        "Consultation responses reviewed by", 
        placeholder="Full name",
        help="Person who reviewed data subject or representative feedback"
    )
    
    st.markdown("#### Final Comments")
    comments = st.text_area(
        "Additional comments", 
        placeholder="Any other notes about this DPIA"
    )
    
    # --- NEW: Validation before submission ---
    submitted = st.form_submit_button("Generate DPIA Report")
    
    if submitted:
        # Validate required fields
        validation_errors = []
        if not measures_approved_by:
            validation_errors.append("Measures approved by (name)")
        if not residual_approved_by:
            validation_errors.append("Residual risks approved by (name)")
        if dpo_advice_provided == "Yes" and not dpo_advice_summary:
            validation_errors.append("Summary of DPO advice")
        if dpo_advice_accepted == "No - overruled" and not overruled_reasons:
            validation_errors.append("Reasons for overruling")
        if not consultation_reviewed_by:
            validation_errors.append("Consultation responses reviewed by")
        
        if validation_errors:
            st.error(f"❌ Please complete the following required fields before generating the report: {', '.join(validation_errors)}")
        else:
            signoff_data = {
                "measures_approved_by": measures_approved_by,
                "date": signoff_date.strftime("%Y-%m-%d"),
                "residual_risks_approved_by": residual_approved_by,
                "dpo_advice_provided": dpo_advice_provided,
                "dpo_advice_summary": dpo_advice_summary,
                "dpo_advice_accepted": dpo_advice_accepted,
                "overruled_reasons": overruled_reasons,
                "consultation_reviewed_by": consultation_reviewed_by,
                "comments": comments
            }
            
            session_data = {
                "need_assessment": st.session_state.get('need_assessment', {}),
                "processing_description": st.session_state.get('processing_description', {})
            }
            
            official_data = st.session_state.get('official_dpia_assessment', {})
            
            try:
                filename = f"dpia_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                pdf_path = generate_dpia_report(
                    session_data, 
                    official_data, 
                    st.session_state.get('risk_register', []), 
                    signoff_data, 
                    filename
                )
                
                st.success("✅ DPIA Report generated successfully!")
                
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download DPIA Report (PDF)",
                        data=f,
                        file_name=filename,
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
                st.info("Please ensure you have reportlab installed: `pip install reportlab`")

st.caption("This sign-off document should be retained as proof of DPIA compliance under GDPR Article 35.")