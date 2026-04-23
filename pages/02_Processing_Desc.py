"""
Step 2: Describe the processing
Based on DPC Sample DPIA Template Step 2
"""

import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Step 2: Processing Description", page_icon="📝")

st.title("📝 Step 2: Describe the Processing")
st.caption("Based on DPC Sample DPIA Template - Step 2")

st.markdown("""
This section documents how personal data will be collected, used, stored, and deleted.
*Source: DPC DPIA guidance - 'Describing the information flows'*
""")

# Initialize processing description in session state
if 'processing_description' not in st.session_state:
    st.session_state.processing_description = {}

# Create form
with st.form("processing_description_form"):
    st.markdown("### Processing Operations")
    
    processing_operations = st.text_area(
        "Describe the processing operations",
        placeholder="What methods will be used for collection, usage, storage, and deletion?",
        help="Outline the type of processing involved"
    )
    
    st.markdown("### Scope of Processing")
    
    data_types = st.text_area(
        "What type of data is involved?",
        placeholder="e.g., names, addresses, financial data, health records...",
        help="List all personal data categories"
    )
    
    special_category = st.radio(
        "Does any data fall under special category (Article 9)?",
        options=["No", "Yes - Health data", "Yes - Biometric data", "Yes - Political/religious", "Yes - Other"],
        help="Special categories include health, biometric, genetic, political opinions, religious beliefs"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        data_volume = st.text_input("Volume of data", placeholder="e.g., 10,000 records, 5GB")
        retention_period = st.text_input("Retention period", placeholder="e.g., 30 days, 5 years")
    with col2:
        individuals_count = st.text_input("Number of individuals affected", placeholder="e.g., 50,000 customers")
        geographic_scope = st.text_input("Geographic scope", placeholder="e.g., Ireland, EU, Global")
    
    st.markdown("### Context of Processing")
    
    relationship = st.text_area(
        "Relationship with data subjects",
        placeholder="e.g., customers, employees, patients, website visitors",
        help="Describe your relationship with the individuals whose data you process"
    )
    
    vulnerable_groups = st.radio(
        "Are vulnerable groups included?",
        options=["No", "Yes - Children", "Yes - Elderly", "Yes - Patients", "Yes - Employees", "Yes - Other vulnerable"],
        help="Vulnerable groups include children, elderly, patients, employees, asylum seekers"
    )
    
    st.markdown("### Purpose of Processing")
    
    purpose = st.text_area(
        "What do you want to achieve?",
        placeholder="Describe the business purpose and intended outcomes",
        help="What benefits will arise from the processing?"
    )
    
    # Submit button
    submitted = st.form_submit_button("Save Processing Description")
    
    if submitted:
        st.session_state.processing_description = {
            "processing_operations": processing_operations,
            "data_types": data_types,
            "special_category": special_category,
            "data_volume": data_volume,
            "retention_period": retention_period,
            "individuals_count": individuals_count,
            "geographic_scope": geographic_scope,
            "relationship": relationship,
            "vulnerable_groups": vulnerable_groups,
            "purpose": purpose,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.success("✅ Processing description saved! Proceed to Step 3 using the sidebar.")

# Display existing data if available
if st.session_state.processing_description:
    with st.expander("📄 View Saved Data"):
        for key, value in st.session_state.processing_description.items():
            if key != "last_updated" and value:
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        st.caption(f"Last updated: {st.session_state.processing_description.get('last_updated', 'N/A')}")

st.caption("Your progress is saved in this session. Use the sidebar to navigate between steps.")