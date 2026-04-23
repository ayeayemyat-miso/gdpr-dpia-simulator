"""
Step 1: Screen for DPIA Requirement Using WP29/EDPB Criteria
Based on WP29 (now EDPB) criteria as cited in DPC guidance
Source: WP248 rev.01 - Guidelines on DPIA
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Step 1: DPIA Screening (WP29 Criteria)", page_icon="🔍")

st.title("🔍 Step 1: Screen for DPIA Requirement")
st.caption("Using WP29 (now EDPB) risk criteria as cited by the Irish Data Protection Commission")

# Info box - no prescriptive order
st.info("""
📌 **Note:** This assessment uses WP29 (now EDPB) risk criteria.

You should also check the **Irish Data Protection Commission's DPIA List** (accessible from the sidebar),
which identifies specific types of processing that automatically require a DPIA.

**Both assessments help determine whether your processing is likely to result in high risk.**
""")

# Combined logic hint
st.caption("""
✅ **A DPIA is required if:**
- Your processing matches the DPC mandatory list (see sidebar), **OR**
- It is likely to result in high risk based on criteria like those below
""")

st.divider()

# The 9 WP29 criteria from WP248 rev.01 pages 9-11
criteria = [
    "Evaluation or scoring (including profiling and predicting), especially from aspects concerning the data subject's performance at work, economic situation, health, personal preferences or interests, reliability or behaviour, location or movements",
    "Automated decision-making with legal or similar significant effect: processing that aims at taking decisions on data subjects producing 'legal effects concerning the natural person' or which 'similarly significantly affects the natural person'",
    "Systematic monitoring: processing used to observe, monitor or control data subjects, including data collected through 'a systematic monitoring of a publicly accessible area'",
    "Processing of sensitive data: this includes special categories of data as defined in Article 9 (e.g., political opinions, health, biometric data), as well as personal data relating to criminal convictions or offenses",
    "Data processed on a large scale (considering: number of data subjects, volume of data, duration of processing, geographical extent)",
    "Matching or combining datasets, for example originating from two or more data processing operations performed for different purposes and/or by different data controllers",
    "Data concerning vulnerable data subjects: children, employees, mentally ill, asylum seekers, elderly, patients, or any case where an imbalance in the relationship exists",
    "Innovative use or applying technological or organisational solutions, like combining use of finger print and face recognition for improved physical access control",
    "Processing that in itself prevents data subjects from exercising a right or using a service or a contract"
]

# Initialize session state
if 'need_assessment' not in st.session_state:
    st.session_state.need_assessment = {}

# Helper text function
def get_help_text(criterion_index):
    help_texts = {
        0: """
        **What this means:**
        Using algorithms or systematic methods to assess, score, or predict people's characteristics, behaviour, or performance.
        
        **Example in banking:**
        A bank screening its customers against a credit reference database to decide creditworthiness.
        *Source: WP248 rev.01, Page 9*
        """,
        1: """
        **What this means:**
        Systems making decisions that have legal consequences or significantly affect people's lives, with no meaningful human involvement.
        
        **Example in banking:**
        An automated system that approves or rejects loan applications without human review.
        *Source: WP248 rev.01, Page 9*
        """,
        2: """
        **What this means:**
        Watching, tracking, or observing people's behaviour or location, especially where they may not be fully aware.
        
        **Example in banking:**
        Monitoring customer transactions for fraud detection or AML compliance.
        *Source: WP248 rev.01, Page 9*
        """,
        3: """
        **What this means:**
        Processing health, biometric, genetic, political, religious, or criminal offence data.
        
        **Example in banking:**
        Processing health data for mortgage insurance applications.
        *Source: WP248 rev.01, Pages 9-10*
        """,
        4: """
        **What this means:**
        Handling data of many people, large volumes, over long periods, or across wide areas.
        
        **Factors to consider:**
        - Number of data subjects
        - Volume of data
        - Duration of processing
        - Geographical extent
        *Source: WP248 rev.01, Page 10*
        """,
        5: """
        **What this means:**
        Merging data from different sources in ways people wouldn't reasonably expect.
        
        **Example in banking:**
        Combining credit bureau data with internal transaction history for fraud detection.
        *Source: WP248 rev.01, Page 10*
        """,
        6: """
        **What this means:**
        Processing data of children, employees, elderly, patients, asylum seekers, or others with power imbalance.
        
        **Example in banking:**
        HR systems processing employee data for performance monitoring.
        *Source: WP248 rev.01, Page 10*
        """,
        7: """
        **What this means:**
        Using AI, IoT, facial recognition, or other new tech where consequences may be unknown.
        
        **Example in banking:**
        Biometric authentication for mobile banking access.
        *Source: WP248 rev.01, Page 10*
        """,
        8: """
        **What this means:**
        Processing that blocks people from accessing services, contracts, or exercising their rights.
        
        **Example in banking:**
        An automated credit decision system that denies service without offering an appeal or human review.
        *Source: WP248 rev.01, Page 11*
        """
    }
    return help_texts.get(criterion_index, "No additional help available for this criterion.")

# Display each criterion
st.markdown("### Does your project involve any of the following?")

responses = {}
for i, criterion_text in enumerate(criteria):
    col1, col2 = st.columns([4, 1])
    with col1:
        short_label = criterion_text[:80] + "..." if len(criterion_text) > 80 else criterion_text
        response = st.radio(
            f"**Criterion {i+1}:** {short_label}",
            options=["No", "Yes"],
            key=f"criterion_{i}",
            horizontal=True
        )
    with col2:
        with st.popover(f"ℹ️ Help for Criterion {i+1}"):
            st.markdown(get_help_text(i))
    responses[f"criterion_{i+1}"] = response == "Yes"

# Helper tip
st.caption("💡 **Tip:** If you are unsure about any criterion, consult your DPO or select 'Yes' as a precaution. The DPC notes that conducting a DPIA when uncertain is still good practice.")

# Warning about contextual factors
st.divider()
st.warning("""
**⚠️ Important - Beyond the Checklist**

A DPIA decision is not purely mechanical. You must also consider:
- **Nature** of the processing (what data, how it's used)
- **Scope** (scale, frequency, duration)
- **Context** (relationship with data subjects, vulnerabilities)
- **Purposes** (what you aim to achieve)

This tool provides an indicative assessment based on WP29 (now EDPB) criteria.
Final determination requires professional judgment.
""")

# Calculate results
yes_count = sum(responses.values())
requires_dpia = yes_count >= 2

# Display recommendation
st.divider()
st.markdown("### 📊 Screening Result")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Risk Indicators Met", f"{yes_count} / 9")
with col2:
    if requires_dpia:
        st.error("🔴 **DPIA Likely Required**")
        st.caption("≥2 criteria = likely high risk")
    else:
        st.success("🟢 **DPIA Not Clearly Indicated**")
        st.caption("<2 criteria = lower risk indicator")
with col3:
    st.caption("Source: WP248 rev.01")

# Legal explanation
st.markdown("#### ℹ️ About This Assessment")
st.info(f"""
**Legal Requirement (GDPR Article 35):**
A DPIA is legally required where processing is **likely to result in a high risk** to the rights and freedoms of natural persons.

**WP29 (now EDPB) Guidance - WP248 rev.01 (as cited by Irish DPC):**
> *"In most cases, a data controller can consider that a processing meeting two criteria would require a DPIA to be carried out."*
> — WP248 rev.01, Page 11

**Your project meets {yes_count} criterion/criteria.**

{'This **indicates a DPIA is likely required**. However, you must also check the official Irish DPC list (see sidebar) and consider the nature, scope, context, and purposes of processing.' if requires_dpia else 'This suggests lower risk, but you must still check the official Irish DPC list (see sidebar) and consider context. Conducting a DPIA is still good practice.'}

*This tool provides an indicative assessment only. Always consult your DPO.*
""")

# Save to session state
st.session_state.need_assessment = {
    "criteria_met": yes_count,
    "recommendation": "DPIA Likely Required" if requires_dpia else "DPIA Not Clearly Indicated (but assess context)",
    "responses": responses,
    "requires_dpia": requires_dpia
}

st.success("✅ Screening complete. Your assessment has been saved.")

# === Regulatory Source Citations ===
st.divider()
with st.expander("📚 Regulatory Sources for This Assessment"):
    st.markdown("""
    **Primary Source: WP29/EDPB Guidelines WP248 rev.01**
    
    The 9 criteria above are derived from the official Article 29 Working Party guidelines:
    
    | Criterion | Source Location in WP248 |
    |-----------|--------------------------|
    | 1. Evaluation or scoring | Page 9, first bullet point |
    | 2. Automated decision-making | Page 9, second bullet point |
    | 3. Systematic monitoring | Page 9, third bullet point |
    | 4. Sensitive data | Pages 9-10, fourth bullet point |
    | 5. Large scale processing | Page 10, fifth bullet point |
    | 6. Matching/combining datasets | Page 10, sixth bullet point |
    | 7. Vulnerable data subjects | Page 10, seventh bullet point |
    | 8. Innovative use/new technology | Page 10, eighth bullet point |
    | 9. Prevents rights or services | Page 11, ninth bullet point |
    
    **Decision Rule (≥2 criteria):**
    > *"In most cases, a data controller can consider that a processing meeting two criteria would require a DPIA to be carried out."*
    — WP248 rev.01, Page 11
    
    **Banking Example (Credit Screening):**
    > *"a financial institution that screens its customers against a credit reference database…"*
    — WP248 rev.01, Page 9
    
    **Full Document Reference:**
    - WP29 (now EDPB), Guidelines on Data Protection Impact Assessment (DPIA) and determining whether processing is 'likely to result in a high risk' for the purposes of Regulation 2016/679, WP248 rev.01, adopted 4 April 2017, revised 4 October 2017
    - Irish Data Protection Commission, List of Types of Data Processing Operations which require a DPIA, November 2018 (revised)
    """)

st.caption("Use the sidebar to navigate to Step 2 (Processing Description) or Step 3 (Risk Register).")