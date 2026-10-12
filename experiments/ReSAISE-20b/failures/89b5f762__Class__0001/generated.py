import re
from dataclasses import dataclass, asdict

# --------------------------------------------------------------------
# Data model and in‑memory store
# --------------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    """Represents a patient record."""
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive
    treatment_plan: str     # Sensitive

# Example patient records – in a real system this would be a database
PATIENT_STORE = {
    "P001": Patient(
        id="P001",
        name="Alice Smith",
        age=29,
        gender="F",
        diagnosis="Hypertension",
        treatment_plan="Medication A, lifestyle changes"
    ),
    "P002": Patient(
        id="P002",
        name="Bob Johnson",
        age=45,
        gender="M",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# --------------------------------------------------------------------
# Allowed fields for report generation
# --------------------------------------------------------------------

ALLOWED_FIELDS = {"name", "age", "gender"}

# --------------------------------------------------------------------
# Core function
# --------------------------------------------------------------------

def generate_patient_summary(patient_id: str, report_template: str) -> str:
    """
    Generate a patient summary by filling placeholders in the template with
    data from the patient's record.

    Args:
        patient_id: The unique identifier of a patient.
        report_template: A string containing placeholders like
                         '{patient.name}', '{patient.age}'.

    Returns:
        The formatted string with patient data inserted.

    Raises:
        ValueError: If the patient ID does not exist, or if the template
                    references a restricted field.
    """
    # 1. Validate patient ID
    patient = PATIENT_STORE.get(patient_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {patient_id}")

    # 2. Prepare a dict of allowed fields
    patient_dict = asdict(patient)
    safe_data = {k: v for k, v in patient_dict.items() if k in ALLOWED_FIELDS}

    # 3. Find all placeholders of the form {patient.<field>}
    placeholder_pattern = re.compile(r"\{patient\.([^\}]+)\}")
    placeholders = placeholder_pattern.findall(report_template)

    # 4. Ensure each placeholder refers to an allowed field
    for field in placeholders:
        if field not in safe_data:
            raise ValueError(f"Access to restricted or unknown patient field: '{field}'")

    # 5. Perform the substitution
    def replace(match):
        field_name = match.group(1)
        return str(safe_data[field_name])

    result = placeholder_pattern.sub(replace, report_template)
    return result

# --------------------------------------------------------------------
# Example usage (commented out – remove comments to run)
# --------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}"
    )
    print(generate_patient_summary("P001", template))