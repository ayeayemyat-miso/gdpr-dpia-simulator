"""
DPIA Process Assistant
Based on Irish Data Protection Commission Guidance and WP29/EDPB Guidelines
"""

import streamlit as st

st.set_page_config(
    page_title="DPIA Process Assistant",
    page_icon="📋",
    layout="wide"
)

# Initialize session state
if 'dpia_session' not in st.session_state:
    st.session_state.dpia_session = {}
if 'risk_register' not in st.session_state:
    st.session_state.risk_register = []

st.title("📋 DPIA Process Assistant")
st.caption("Based on Irish Data Protection Commission (DPC) Guidance and WP29/EDPB Guidelines (WP248 rev.01)")

# Introduction
with st.expander("ℹ️ What is a Data Protection Impact Assessment (DPIA)?", expanded=True):
    st.markdown("""
    A **Data Protection Impact Assessment (DPIA)** is a process designed to identify risks arising out of the 
    processing of personal data and to minimise these risks as far and as early as possible.
    
    ### Why conduct a DPIA?
    - Ensure and demonstrate compliance with the GDPR
    - Inspire public confidence in your data handling
    - Protect individuals' data protection rights
    - Enable "data protection by design"
    - Reduce operational costs by optimising information flows
    - Minimise data protection related risks to your organisation
    """)

# DPIA Process
with st.expander("📚 DPIA Process (Based on DPC Guidance)"):
    st.markdown("""
    **Typical DPIA Process based on Irish DPC guidance:**
    
    1. **Screening** – Determine if a DPIA is required (WP29/EDPB criteria)
    2. **Describe the processing** – Purpose, scope, context, and data flows
    3. **Consultation** – Engage with DPO (mandatory if appointed) and stakeholders; data subjects where appropriate
    4. **Assess necessity and proportionality** – Lawful basis, data minimisation, retention
    5. **Identify and assess risks** – Impact on individuals' rights and freedoms
    6. **Identify mitigation measures** – Controls to reduce or eliminate risks
    7. **Document outcomes and approval** – Record decisions, ensure accountability
    8. **Consult the DPC if needed** – Required under GDPR Article 36 if high risks remain unresolved
    
    *Source: Irish Data Protection Commission*
    """)

# Sidebar navigation info
st.sidebar.header("🚀 Navigation")
st.sidebar.info("""
Use the sidebar to navigate through the DPIA process:

1. **Official Irish DPIA List** - Mandatory DPC criteria
2. **WP29 Risk Criteria** - 9-criteria assessment
3. **Processing Description** - Document data flows
4. **Risk Register** - Identify and assess risks
5. **Report & Sign-Off** - Generate final report
""")

# Navigation buttons
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Quick Start")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("📋 Irish List", use_container_width=True):
        st.switch_page("pages/00_Official_Irish_List.py")
with col2:
    if st.button("🔍 WP29 Criteria", use_container_width=True):
        st.switch_page("pages/01_Need_Assessment.py")

# --- NEW: Reset All Data Button ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧹 Data Management")
if st.sidebar.button("🗑️ Reset All Data", use_container_width=True, type="secondary"):
    # Clear all session state keys
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    # Re-initialize empty structures
    st.session_state.dpia_session = {}
    st.session_state.risk_register = []
    st.sidebar.success("✅ All data cleared! Refresh to start over.")
    st.rerun()

# === Regulatory Sources ===
st.divider()
st.markdown("""
### 📚 Regulatory Framework

This tool implements two complementary DPIA assessment frameworks:

| Framework | Source | Legal Basis |
|-----------|--------|-------------|
| **Official Irish DPIA List** | Irish DPC, November 2018 | GDPR Article 35(4) |
| **WP29/EDPB Risk Criteria** | WP248 rev.01, October 2017 | GDPR Article 35(1) |

**Key References:**
1. European Data Protection Board, *Guidelines on Data Protection Impact Assessment (DPIA) and determining whether processing is 'likely to result in a high risk'* (WP248 rev.01), 4 October 2017
2. Irish Data Protection Commission, *List of Types of Data Processing Operations which require a Data Protection Impact Assessment*, November 2018 (revised)
3. GDPR Article 35 - Data Protection Impact Assessment
4. GDPR Article 36 - Prior Consultation

---
*This tool is for educational and professional portfolio purposes. Always consult your Data Protection Officer for official DPIAs.*
""")