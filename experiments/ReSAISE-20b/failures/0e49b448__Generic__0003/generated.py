import re
from dataclasses import dataclass, fields
from typing import Dict

# ----------------------------------------------------------------------
# Sample in‑memory patient database (for demonstration purposes)
# In a real system this would be replaced by persistent storage.
# ----------------------------------------------------------------------
@dataclass
class Patient:
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive
    treatment_plan: str     # Sensitive

# Example patient records keyed by a unique identifier.
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        name="Alice Smith",
        age=34,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "P002": Patient(
        name="Bob Johnson",
        age=58,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# ----------------------------------------------------------------------
# Function to build a patient summary from a template string
# ----------------------------------------------------------------------
def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Generate a patient summary string by applying `template_string` to the
    non-sensitive attributes of the patient identified by `patient_key`.

    Parameters:
        patient_key (str): Identifier for the patient.
        template_string (str): Template containing placeholders like
                               '{patient.name}', '{patient.age}'.

    Returns:
        str: The formatted summary string.

    Raises:
        ValueError: If the patient ID is unknown or if the template tries
                    to access sensitive fields (diagnosis, treatment_plan).
    """
    # 1. Retrieve the patient record
    patient = PATIENT_DB.get(patient_key)
    if not patient:
        raise ValueError(f"Patient ID '{patient_key}' not found.")

    # 2. Detect placeholders in the template
    placeholder_pattern = re.compile(r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}")
    placeholders = placeholder_pattern.findall(template_string)

    # 3. Check for access to sensitive fields
    SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
    for field in placeholders:
        if field in SENSITIVE_FIELDS:
            raise ValueError(
                f"Access to sensitive patient information '{field}' is not allowed."
            )

    # 4. Build a mapping of non-sensitive attributes
    allowed_fields = {
        f.name for f in fields(Patient) if f.name not in SENSITIVE_FIELDS
    }
    patient_data = {
        key: getattr(patient, key) for key in allowed_fields
    }

    # 5. Perform the substitution using str.format_map
    try:
        summary = template_string.format(patient=patient_data)
    except KeyError as exc:
        missing_field = exc.args[0]
        raise ValueError(
            f"Template references unknown patient field '{missing_field}'."
        ) from None

    return summary