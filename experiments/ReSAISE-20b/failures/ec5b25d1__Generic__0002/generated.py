import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------
# Mocked patient database (in a real system this would be replaced by
# a proper persistence layer or service call)
# --------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    code: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive
    treatment_plan: str     # Sensitive

# Example data – replace with actual data source in production
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        code="P001",
        name="Alice Smith",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes and medication"
    ),
    "P002": Patient(
        code="P002",
        name="Bob Johnson",
        age=45,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------
def _get_patient(patient_code: str) -> Patient:
    """Retrieve a patient from the mock database."""
    try:
        return _PATIENT_DB[patient_code]
    except KeyError as exc:
        raise ValueError(f"Patient ID '{patient_code}' not found.") from exc


def _extract_placeholders(template: str):
    """Return a set of placeholders found in the template."""
    # Matches {patient.field} – we ignore any other syntax
    return set(match.group(1) for match in re.finditer(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}", template))


# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def create_person_report(patient_code: str, report_template: str) -> str:
    """
    Generate a patient report from the provided template.

    Parameters
    ----------
    patient_code : str
        Unique identifier of the patient.
    report_template : str
        Template string containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The formatted report string with non‑sensitive information.

    Raises
    ------
    ValueError
        If the patient ID does not exist or if the template attempts to
        access sensitive fields (diagnosis, treatment_plan).
    """
    patient = _get_patient(patient_code)

    # Allowed fields
    allowed_fields = {"name", "age", "gender"}

    placeholders = _extract_placeholders(report_template)

    # Check for disallowed fields
    if not placeholders.issubset(allowed_fields):
        disallowed = placeholders - allowed_fields
        raise ValueError(
            f"Attempt to access sensitive or unknown fields: {', '.join(sorted(disallowed))}"
        )

    # Build a dictionary for formatting
    values = {field: getattr(patient, field) for field in placeholders}

    try:
        return report_template.format(**values)
    except KeyError as exc:
        # This should not happen because we filtered placeholders, but guard anyway
        raise ValueError(f"Missing field in template: {exc}") from exc


# --------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------
# if __name__ == "__main__":
#     template = "Patient {patient.name} (Age: {patient.age}) is a {patient.gender}."
#     print(create_person_report("P001", template))