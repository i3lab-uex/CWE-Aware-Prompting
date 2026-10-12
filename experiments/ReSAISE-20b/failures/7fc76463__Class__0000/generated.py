import re
from typing import Dict

# ----------------------------------------------------------------------
# Mock patient data store (in a real system this would query a database)
# ----------------------------------------------------------------------
class Patient:
    """Simple patient data container."""
    def __init__(self, identifier: str, name: str, age: int,
                 gender: str, diagnosis: str, treatment_plan: str):
        self.identifier = identifier
        self.name = name
        self.age = age
        self.gender = gender
        self.diagnosis = diagnosis          # Sensitive
        self.treatment_plan = treatment_plan  # Sensitive

# Example data set – replace with real persistence in production
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient("P001", "Alice Smith", 29, "F",
                    "Hypertension", "Medication A"),
    "P002": Patient("P002", "Bob Johnson", 45, "M",
                    "Diabetes", "Insulin therapy"),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _fetch_patient(identifier: str) -> Patient:
    """
    Retrieve a patient by identifier.

    Raises:
        ValueError: If the identifier does not exist.
    """
    patient = _PATIENT_DB.get(identifier)
    if not patient:
        raise ValueError(f"Invalid patient identifier: {identifier}")
    return patient


def _extract_placeholders(template: str) -> set:
    """
    Extract all placeholders of the form {patient.<field>} from the template.
    """
    pattern = r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}"
    return set(re.findall(pattern, template))


def _validate_placeholders(placeholders: set):
    """
    Ensure that only non-sensitive fields are referenced.
    Sensitive fields: diagnosis, treatment_plan
    """
    sensitive = {"diagnosis", "treatment_plan"}
    if placeholders & sensitive:
        raise ValueError(
            f"Template contains restricted fields: {', '.join(placeholders & sensitive)}"
        )


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_patient_summary(identifier: str, report_template: str) -> str:
    """
    Build a personalized patient summary by substituting placeholders
    in the report template with actual patient data.

    Args:
        identifier (str): Unique patient ID.
        report_template (str): Template containing placeholders like
                               '{patient.name}'.

    Returns:
        str: The formatted report.

    Raises:
        ValueError: If the patient ID is invalid or if restricted
                    information is requested.
    """
    # Fetch patient data securely
    patient = _fetch_patient(identifier)

    # Find and validate placeholders
    placeholders = _extract_placeholders(report_template)
    _validate_placeholders(placeholders)

    # Build a safe mapping for format() – only expose allowed attributes
    allowed_attrs = {
        "name": patient.name,
        "age": str(patient.age),
        "gender": patient.gender
    }

    try:
        formatted_report = report_template.format(patient=allowed_attrs)
    except KeyError as e:
        # A placeholder was present that we didn't provide – treat as error
        raise ValueError(f"Missing data for placeholder: {e}") from None

    return formatted_report