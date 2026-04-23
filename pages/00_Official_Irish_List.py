"""
Step 0: Official Irish DPC DPIA List (Article 35(4))
Based on DPC adopted list - November 2018
Source: https://www.dataprotection.ie/sites/default/files/uploads/2018-11/Data-Protection-Impact-Assessment.pdf
"""

import streamlit as st

st.set_page_config(page_title="Official Irish DPIA List", page_icon="⚖️")

st.title("⚖️ Official Irish DPIA List")
st.caption("Adopted by the Data Protection Commission under GDPR Article 35(4) - November 2018")

st.markdown("""
The following types of processing operations **require a DPIA** where a documented screening 
indicates they are likely to result in a high risk to individuals' rights and freedoms.

*Source: DPC - List of Types of Data Processing Operations which require a DPIA (page 4)*
""")

# The 10 official criteria from page 4 of the PDF
official_criteria = [
    "Use of personal data on a large-scale for a purpose(s) other than that for which it was initially collected (GDPR Article 6(4))",
    "Profiling vulnerable persons including children to target marketing or online services at such persons",
    "Use of profiling or algorithmic means or special category data as an element to determine access to services or that results in legal or similarly significant effects",
    "Systematically monitoring, tracking or observing individuals' location or behaviour",
    "Profiling individuals on a large-scale",
    "Processing biometric data to uniquely identify an individual in combination with any other WP29 criteria",
    "Processing genetic data in combination with any other WP29 criteria",
    "Indirectly sourcing personal data where GDPR transparency requirements are not being met",
    "Combining, linking or cross-referencing separate datasets where used for profiling or behavioural analysis",
    "Large scale processing where the Data Protection Act 2018 requires 'suitable and specific measures'"
]

st.markdown("### Does your processing operation fall into any of these categories?")
st.caption("Answer honestly. These are legally adopted criteria by the Irish DPC.")

responses = {}
for i, criterion in enumerate(official_criteria, 1):
    response = st.radio(
        f"**{i}.** {criterion}",
        options=["No", "Yes"],
        key=f"official_{i}",
        horizontal=True
    )
    responses[i] = response == "Yes"

yes_count = sum(responses.values())

st.divider()
st.markdown("### 📊 Assessment Result")

col1, col2 = st.columns(2)
with col1:
    st.metric("Official Criteria Matched", f"{yes_count} / 10")

with col2:
    if yes_count >= 1:
        st.error("🔴 **DPIA Required Under Irish Law**")
    else:
        st.success("🟢 **Not on Official List**")

if yes_count >= 1:
    st.warning(f"""
    **DPIA Required Under Irish Law**
    
    Your processing operation matches **{yes_count} item(s)** on the official Irish DPC list adopted under GDPR Article 35(4).
    
    You **must conduct a DPIA** before commencing this processing.
    """)
else:
    st.info("""
    **Not on Official List - But Continue Assessment**
    
    Your operation does not match any item on the official Irish DPIA list.
    
    However, under GDPR Article 35(1), you must still assess whether the processing is **likely to result in high risk** 
    to individuals' rights and freedoms. Proceed to **Step 1 (WP29 Criteria)** for the supplementary assessment.
    """)

# Save to session state
if 'official_dpia_assessment' not in st.session_state:
    st.session_state.official_dpia_assessment = {
        "criteria_met": yes_count,
        "requires_dpia": yes_count >= 1,
        "responses": responses,
        "source": "DPC Article 35(4) List (November 2018)"
    }

st.success("✅ Assessment saved. Use the sidebar to proceed to the WP29 Criteria assessment.")

# === Regulatory Source Citations ===
st.divider()
with st.expander("📚 Regulatory Sources for the Official Irish List"):
    st.markdown("""
    **Primary Source: Irish Data Protection Commission**
    
    The 10 criteria above are the official Irish DPIA list adopted under **GDPR Article 35(4)**.
    
    | Criterion | Source |
    |-----------|--------|
    | 1-10 | DPC DPIA List, Page 4 |
    
    **Legal Basis:**
    > *"Pursuant to Article 35(4) of the General Data Protection Regulation (GDPR), the Irish Data Protection Commission adopts the following list specifying the types of processing operations subject to the requirement for a Data Protection Impact Assessment (DPIA)."*
    — DPC DPIA List, Page 2
    
    **Relationship to WP29/EDPB Guidelines:**
    > *"The criteria developed in the WP29 DPIA Guidelines were applied in the development and approval of this list to support the consistent application of the GDPR."*
    — DPC DPIA List, Page 3
    
    **Full Document Reference:**
    - Data Protection Commission (Ireland), List of Types of Data Processing Operations which require a Data Protection Impact Assessment, November 2018 (revised)
    - Available at: https://www.dataprotection.ie/sites/default/files/uploads/2018-11/Data-Protection-Impact-Assessment.pdf
    """)

st.caption("Use the sidebar to navigate to the WP29 Criteria assessment or continue to Step 2.")