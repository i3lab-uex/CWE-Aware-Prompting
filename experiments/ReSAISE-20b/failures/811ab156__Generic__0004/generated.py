import re
from typing import Dict

# ------------------------------------------------------------------
# Dummy patient storage for demonstration purposes.
# In a real system this would query a database or an external service.
# ------------------------------------------------------------------
class Patient:
    def __init__(self, identifier: str, name: str, age: int,
                 gender: str, diagnosis: str, treatment_plan: str):
        self.identifier = identifier
        self.name = name
        self.age = age
        self.gender = gender
        self.diagnosis = diagnosis
        self.treatment_plan = treatment_plan

# Example in‑memory patient database
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient("P001", "Alice Smith", 29, "Female",
                    "Hypertension", "Medication and lifestyle changes"),
    "P002": Patient("P002", "Bob Johnson", 45, "Male",
                    "Type II Diabetes", "Insulin therapy"),
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def _get_patient(patient_id: str) -> Patient:
    """
    Retrieve a patient object from the database.
    Raises ValueError if the ID is not found.
    """
    patient = _PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Invalid patient identifier: {patient_id!r}")
    return patient

def _extract_placeholders(template: str):
    """
    Return a set of placeholder names found in the template.
    Placeholders are expected to be in the form `{patient.<field>}`.
    """
    pattern = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    return set(pattern.findall(template))

def _build_replacements(patient: Patient, placeholders: set):
    """
    Build a dictionary mapping placeholder names to patient attribute values.
    Raises ValueError if any placeholder does not exist on the patient object.
    """
    replacements = {}
    for field in placeholders:
        if not hasattr(patient, field):
            raise ValueError(f"Unknown patient attribute requested: {field!r}")
        replacements[field] = getattr(patient, field)
    return replacements

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def assemble_patient_report(patient_identifier: str, report_template: str) -> str:
    """
    Assemble a personalized patient report by replacing placeholders in the
    provided template with actual patient data.

    Parameters:
        patient_identifier (str): Unique identifier of the patient.
        report_template (str): Report template containing placeholders like
                               `{patient.name}`, `{patient.age}`, etc.

    Returns:
        str: The formatted report with all placeholders substituted.

    Raises:
        ValueError: If the patient ID is invalid, if restricted fields are
                    requested in the template, or if a placeholder refers to
                    an unknown attribute.
    """
    # 1. Validate and fetch patient data
    patient = _get_patient(patient_identifier)

    # 2. Identify placeholders in the template
    placeholders = _extract_placeholders(report_template)

    # 3. Enforce security: restrict access to sensitive fields
    RESTRICTED_FIELDS = {"diagnosis", "treatment_plan"}
    if placeholders & RESTRICTED_FIELDS:
        restricted = ", ".join(sorted(placeholders & RESTRICTED_FIELDS))
        raise ValueError(f"Attempt to access restricted patient data: {restricted}")

    # 4. Build mapping of placeholder -> value
    replacements = _build_replacements(patient, placeholders)

    # 5. Perform the substitution safely
    def replace_match(match):
        field_name = match.group(1)
        return str(replacements.get(field_name, f"<missing:{field_name}>"))

    safe_pattern = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    formatted_report = safe_pattern.sub(replace_match, report_template)

    return formatted_report

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Patient Report\n"
#         "Name: {patient.name}\n"
#         "Age: {patient.age}\n"
#         "Gender: {patient.gender}\n"
#     )
#     print(assemble_patient_report("P001", template))