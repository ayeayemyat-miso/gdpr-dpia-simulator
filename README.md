# GDPR DPIA Simulator
## Live Demo
[https://gdpr-dpia-simulator-dm6r35ojskanhbogvcecek.streamlit.app/]

## What This Project Does
A decision-support tool for Irish financial services firms to determine if a Data Protection Impact Assessment (DPIA) is required for a new project under GDPR.

## Why I Built This
DPIAs are mandatory under GDPR for high-risk processing. Many firms struggle to consistently apply the 9 screening criteria. This tool automates the initial assessment.

## Regulatory Sources

This tool implements two layers of DPIA assessment:

1. **Official Irish DPC List (Primary)** - Adopted under GDPR Article 35(4), November 2018
   - Source: https://www.dataprotection.ie/sites/default/files/uploads/2018-11/Data-Protection-Impact-Assessment.pdf

2. **WP29/EDPB Guidelines (Secondary)** - As cited by the Irish DPC
   - The "≥2 criteria" rule of thumb for identifying high risk

## Scoring Logic
- 0-4 points: DPIA not required
- 5-8 points: Further review needed
- 9+ points: DPIA required

## How to Run
1. Clone this repo
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

