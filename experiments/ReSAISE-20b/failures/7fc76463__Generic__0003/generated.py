import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
#  Patient model and a simple in‑memory registry (mock database)
# ----------------------------------------------------------------------
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# A mock patient registry. In a real system this would be replaced by
# database queries and proper authentication/authorization checks.
PATIENT_REGISTRY: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lisinopril 10mg daily"
    ),
    "P002": Patient(
        patient_id="P002",
        name="Jane Smith",
        age=32,
        gender="Female",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Metformin 500mg twice daily"
    ),
}

# ----------------------------------------------------------------------
#  Utility functions
# ----------------------------------------------------------------------
def _get_patient(identifier: str) -> Patient:
    """
    Retrieve a patient from the registry.
    Raises ValueError if the identifier is unknown.
    """
    patient = PATIENT_REGISTRY.get(identifier)
    if not patient:
        raise ValueError(f"Invalid patient ID: {identifier}")
    return patient

def _extract_placeholders(template: str):
    """
    Return a set of placeholder keys found in the template.
    Placeholders are expected to be in the form `{patient.<field>}`.
    """
    return set(re.findall(r'\{([^}]+)\}', template))

def _build_context(patient: Patient, placeholders):
    """
    Build a dictionary mapping placeholder names to patient attributes.
    Raises ValueError if restricted fields are requested or
    if a placeholder does not correspond to an attribute.
    """
    # Fields that are considered restricted (no direct access allowed)
    RESTRICTED_FIELDS = {"diagnosis", "treatment_plan"}

    context = {}
    for key in placeholders:
        # Expect keys to be of the form patient.<field>
        if not key.startswith("patient."):
            raise ValueError(f"Invalid placeholder format: {key}")
        field_name = key.split(".", 1)[1]

        if field_name in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{field_name}' is not allowed")

        if not hasattr(patient, field_name):
            raise ValueError(f"Unknown patient attribute: {field_name}")

        context[key] = getattr(patient, field_name)
    return context

# ----------------------------------------------------------------------
#  Public API
# ----------------------------------------------------------------------
def build_patient_summary(identifier: str, report_template: str) -> str:
    """
    Generate a personalized patient summary by replacing placeholders
    in the provided report template with actual patient data.

    Parameters:
        identifier (str): Unique patient ID.
        report_template (str): Report template containing placeholders.

    Returns:
        str: The formatted report string.

    Raises:
        ValueError: If the patient ID is invalid, if restricted
                    medical information is requested, or if a placeholder
                    does not match any patient attribute.
    """
    # Retrieve the patient record
    patient = _get_patient(identifier)

    # Find all placeholders in the template
    placeholders = _extract_placeholders(report_template)
    if not placeholders:
        # No placeholders to replace; return template as is
        return report_template

    # Build the context dictionary for formatting
    context = _build_context(patient, placeholders)

    # Perform substitution safely
    try:
        formatted_report = report_template.format(**context)
    except KeyError as exc:
        # This should not happen because we pre‑validated placeholders
        raise ValueError(f"Missing placeholder value: {exc}") from exc

    return formatted_report