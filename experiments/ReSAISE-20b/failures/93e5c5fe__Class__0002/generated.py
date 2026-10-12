import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
# Patient model and in‑memory registry (for demonstration purposes)
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    uid: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive
    treatment_plan: str     # Sensitive

# In a real system this would be replaced by a database query
_PATIENT_REGISTRY: Dict[str, Patient] = {
    "patient-001": Patient(
        uid="patient-001",
        name="Alice Smith",
        age=29,
        gender="F",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes and medication"
    ),
    "patient-002": Patient(
        uid="patient-002",
        name="Bob Johnson",
        age=45,
        gender="M",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
_ALLOWED_PLACEHOLDERS_RE = re.compile(r"\{([^{}]+)\}")

def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in _ALLOWED_PLACEHOLDERS_RE.finditer(template)}

def _patient_to_dict(patient: Patient) -> Dict[str, str]:
    """Return a dictionary containing only non-sensitive patient data."""
    full_dict = asdict(patient)
    # Remove sensitive fields
    for field in _SENSITIVE_FIELDS:
        full_dict.pop(field, None)
    # Prefix keys with 'patient.' to match template syntax
    prefixed = {f"patient.{k}": v for k, v in full_dict.items()}
    return prefixed

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Compose a patient report by filling the provided template with
    non-sensitive data from the specified patient.

    Parameters:
        patient_uid (str): The unique identifier of the patient.
        report_schema (str): A template string containing placeholders
                             such as '{patient.name}'.

    Returns:
        str: The formatted report string.

    Raises:
        ValueError: If the patient UID is unknown or if the template
                    references a sensitive field.
    """
    # Retrieve patient record
    patient = _PATIENT_REGISTRY.get(patient_uid)
    if not patient:
        raise ValueError(f"Patient with UID '{patient_uid}' not found.")

    # Extract placeholders from the template
    placeholders = _extract_placeholders(report_schema)

    # Check for disallowed (sensitive) fields
    sensitive_in_template = {
        ph.split(".")[1] for ph in placeholders if "." in ph
    } & _SENSITIVE_FIELDS
    if sensitive_in_template:
        raise ValueError(
            f"Template attempts to access sensitive fields: {', '.join(sensitive_in_template)}"
        )

    # Prepare mapping for formatting
    patient_data = _patient_to_dict(patient)

    try:
        report = report_schema.format_map(patient_data)
    except KeyError as exc:
        # Placeholder not found in patient data
        raise ValueError(f"Unknown placeholder: {exc}") from None

    return report

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = "Patient {patient.name} (Age: {patient.age}, Gender: {patient.gender})"
#     print(compose_patient_report("patient-001", template))