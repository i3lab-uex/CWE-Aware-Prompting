import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Simulated data store and patient model
# ------------------------------------------------------------------

@dataclass
class Patient:
    """Simple representation of a patient's data."""
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str
    # Sensitive data that should never be exposed via a public report
    medical_history: str = field(repr=False, default="")
    ssn: str = field(repr=False, default="")

# In‑memory patient registry for demonstration purposes
PATIENT_REGISTRY: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="Alice Smith",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle modification, medication",
        medical_history="Previous heart attack in 2018.",
        ssn="123-45-6789",
    ),
    "P002": Patient(
        patient_id="P002",
        name="Bob Johnson",
        age=45,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Metformin, diet plan",
        medical_history="Family history of diabetes.",
        ssn="987-65-4321",
    ),
}

# ------------------------------------------------------------------
# Core functionality
# ------------------------------------------------------------------

ALLOWED_FIELDS = {
    "name",
    "age",
    "gender",
    "diagnosis",
    "treatment_plan",
}

PLACEHOLDER_PATTERN = re.compile(r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}")

def assemble_patient_report(patient_identifier: str, report_template: str) -> str:
    """
    Generate a personalized patient report by replacing placeholders in the
    template with actual patient data.

    Parameters
    ----------
    patient_identifier : str
        The unique identifier of the patient.
    report_template : str
        Template string containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The fully formatted report.

    Raises
    ------
    ValueError
        If the patient ID is not found or if a restricted field is accessed.
    """
    # 1. Retrieve patient
    patient = PATIENT_REGISTRY.get(patient_identifier)
    if not patient:
        raise ValueError(f"Patient ID '{patient_identifier}' is invalid.")

    # 2. Find all placeholders
    matches = PLACEHOLDER_PATTERN.findall(report_template)
    if not matches:
        # No placeholders, return template as is
        return report_template

    # 3. Validate and replace each placeholder
    def replacement(match: re.Match) -> str:
        field_name = match.group(1)
        if field_name not in ALLOWED_FIELDS:
            raise ValueError(
                f"Access to restricted or unknown field '{field_name}' is not permitted."
            )
        value = getattr(patient, field_name)
        return str(value)

    # 4. Perform substitution
    formatted_report = PLACEHOLDER_PATTERN.sub(replacement, report_template)

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
#         "Diagnosis: {patient.diagnosis}\n"
#         "Treatment Plan: {patient.treatment_plan}"
#     )
#     print(assemble_patient_report("P001", template))