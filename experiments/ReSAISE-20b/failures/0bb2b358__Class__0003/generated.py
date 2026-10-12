import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------
# 1. Patient data model (stub)
# ------------------------------
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive
    treatment_plan: str     # Sensitive

# ------------------------------
# 2. In‑memory patient store (example)
# ------------------------------
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "P002": Patient(
        patient_id="P002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# ------------------------------
# 3. Allowed template placeholders
# ------------------------------
_ALLOWED_FIELDS = {"patient.name", "patient.age", "patient.gender"}

_TEMPLATE_PATTERN = re.compile(r"{([^}]+)}")

# ------------------------------
# 4. Report generation
# ------------------------------
def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report for the specified patient by substituting allowed placeholders
    in the provided template with actual patient data.

    Parameters:
        patient_id (str): Identifier of the patient.
        template   (str): Report template containing placeholders.

    Returns:
        str: The formatted report string.

    Raises:
        ValueError: If the patient does not exist, the template contains
                    disallowed placeholders, or any other error occurs.
    """
    # Retrieve patient record
    patient = _PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Patient with ID '{patient_id}' not found")

    # Find all placeholders in the template
    placeholders = set(match.group(1) for match in _TEMPLATE_PATTERN.finditer(template))

    # Validate placeholders
    disallowed = placeholders - _ALLOWED_FIELDS
    if disallowed:
        raise ValueError(
            f"Disallowed placeholders detected: {', '.join(sorted(disallowed))}"
        )

    # Build a mapping for allowed fields
    field_map = {
        "patient.name": patient.name,
        "patient.age": str(patient.age),
        "patient.gender": patient.gender
    }

    # Perform safe substitution
    try:
        report = template.format(**field_map)
    except KeyError as exc:
        raise ValueError(f"Missing field in template: {exc}") from None
    except Exception as exc:
        raise ValueError(f"Template formatting error: {exc}") from None

    return report