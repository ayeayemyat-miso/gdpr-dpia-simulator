"""
Step 3: Identify and assess risks (Risk Register)
Based on DPC Sample DPIA Template Step 5
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Step 3: Risk Register", page_icon="⚠️")

st.title("⚠️ Step 3: Risk Register")
st.caption("Based on DPC Sample DPIA Template - Step 5: Identify and assess risks")

st.markdown("""
This register documents data protection risks, their likelihood, severity, and overall risk level.
*Source: DPC DPIA guidance - 'Identifying data protection and related risks'*
""")

# Initialize risk register in session state
if 'risk_register' not in st.session_state:
    st.session_state.risk_register = []

# Risk scoring functions
def calculate_overall_risk(likelihood, severity):
    risk_matrix = {
        ("Remote", "Minimal"): "Low",
        ("Remote", "Significant"): "Low",
        ("Remote", "Severe"): "Medium",
        ("Possible", "Minimal"): "Low",
        ("Possible", "Significant"): "Medium",
        ("Possible", "Severe"): "High",
        ("Probable", "Minimal"): "Medium",
        ("Probable", "Significant"): "High",
        ("Probable", "Severe"): "High",
    }
    return risk_matrix.get((likelihood, severity), "Medium")

# Example risks from DPC page
EXAMPLE_RISKS = [
    "Inappropriate disclosure of personal data internally",
    "Accidental loss of electronic equipment",
    "Data breach by hackers",
    "Vulnerable individuals affected by disclosure",
    "Data used in unanticipated ways",
    "Automated decision-making seen as intrusive",
    "Merging datasets revealing unexpected information",
    "GDPR non-compliance leading to fines",
    "Reputational damage",
    "Compensation claims from individuals"
]

# Sidebar with example risks
with st.sidebar:
    st.markdown("### 📋 Example Risks (from DPC guidance)")
    for risk in EXAMPLE_RISKS[:5]:
        st.write(f"• {risk}")
    with st.expander("More examples"):
        for risk in EXAMPLE_RISKS[5:]:
            st.write(f"• {risk}")

# Form to add new risk
with st.form("add_risk_form"):
    st.markdown("### ➕ Add New Risk")
    
    risk_description = st.text_area("Risk Description", placeholder="Describe the risk...")
    
    col1, col2 = st.columns(2)
    with col1:
        likelihood = st.selectbox("Likelihood of Harm", ["Remote", "Possible", "Probable"])
    with col2:
        severity = st.selectbox("Severity of Harm", ["Minimal", "Significant", "Severe"])
    
    overall_risk = calculate_overall_risk(likelihood, severity)
    st.info(f"**Calculated Overall Risk:** {overall_risk}")
    
    mitigation = st.text_area("Proposed Mitigation Measures", placeholder="How can this risk be reduced or eliminated?")
    
    submitted = st.form_submit_button("Add Risk")
    
    if submitted and risk_description:
        new_risk = {
            "id": len(st.session_state.risk_register),
            "description": risk_description,
            "likelihood": likelihood,
            "severity": severity,
            "overall_risk": overall_risk,
            "mitigation": mitigation
        }
        st.session_state.risk_register.append(new_risk)
        st.success(f"Risk added!")
        st.rerun()

# Display current risk register
st.markdown("### 📋 Current Risk Register")

if st.session_state.risk_register:
    df = pd.DataFrame(st.session_state.risk_register)
    display_df = df[["id", "description", "likelihood", "severity", "overall_risk", "mitigation"]]
    st.dataframe(display_df, use_container_width=True)
    
    # Delete functionality
    st.markdown("#### 🗑️ Delete a Risk")
    risk_to_delete = st.selectbox(
        "Select risk to delete",
        options=[(r["id"], r["description"][:50]) for r in st.session_state.risk_register],
        format_func=lambda x: f"ID {x[0]}: {x[1]}"
    )
    if st.button("Delete Selected Risk"):
        st.session_state.risk_register = [r for r in st.session_state.risk_register if r["id"] != risk_to_delete[0]]
        st.success("Risk deleted!")
        st.rerun()
    
    # Summary statistics
    st.markdown("### 📊 Risk Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        high_risks = len([r for r in st.session_state.risk_register if r["overall_risk"] == "High"])
        st.metric("High Risks", high_risks)
    with col2:
        medium_risks = len([r for r in st.session_state.risk_register if r["overall_risk"] == "Medium"])
        st.metric("Medium Risks", medium_risks)
    with col3:
        low_risks = len([r for r in st.session_state.risk_register if r["overall_risk"] == "Low"])
        st.metric("Low Risks", low_risks)
else:
    st.info("No risks added yet. Use the form above to add risks to your register.")

# Save to CSV option
if st.session_state.risk_register:
    if st.button("💾 Save Risk Register to CSV"):
        df = pd.DataFrame(st.session_state.risk_register)
        df.to_csv("data/risk_register.csv", index=False)
        st.success("Saved to data/risk_register.csv")

st.caption("Your progress is saved in this session. Proceed to Step 4 using the sidebar.")