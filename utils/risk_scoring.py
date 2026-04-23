"""
Risk scoring utilities based on DPC DPIA guidance Step 5
Source: https://www.dataprotection.ie/en/organisations/know-your-obligations/data-protection-impact-assessments
"""

def assess_likelihood(description):
    """
    Assess the likelihood of harm based on description.
    Returns: "Remote", "Possible", or "Probable"
    """
    # Simple rule-based assessment
    # In a real app, this would be more sophisticated
    # For now, return "Possible" as default - user can edit
    return "Possible"


def assess_severity(description):
    """
    Assess the severity of harm based on description.
    Returns: "Minimal", "Significant", or "Severe"
    """
    # Simple rule-based assessment
    # For now, return "Significant" as default - user can edit
    return "Significant"


def calculate_overall_risk(likelihood, severity):
    """
    Calculate overall risk based on likelihood and severity.
    Based on DPC Step 5 matrix.
    
    Likelihood: Remote, Possible, Probable
    Severity: Minimal, Significant, Severe
    
    Returns: "Low", "Medium", or "High"
    """
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


# Example risks from DPC page (for reference)
EXAMPLE_RISKS_TO_INDIVIDUALS = [
    "Inappropriate disclosure of personal data internally",
    "Accidental loss of electronic equipment",
    "Data breach by hackers",
    "Vulnerable individuals affected by disclosure",
    "Anonymised data leading to re-identification",
    "Data used in unanticipated ways",
    "Automated decision-making seen as intrusive",
    "Merging datasets revealing unexpected information"
]

CORPORATE_RISKS = [
    "GDPR non-compliance leading to fines",
    "Reputational damage",
    "Public distrust",
    "Expensive late-stage fixes",
    "Compensation claims from individuals"
]