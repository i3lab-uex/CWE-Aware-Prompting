import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
# Patient model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    """Immutable representation of a patient record."""
    code: str
    name: str
    age: int
    gender: str
    # Sensitive fields – should never be exposed through create_person_report
    diagnosis: str
    treatment_plan: str


# ----------------------------------------------------------------------
# In‑memory patient repository (simulating a database)
# ----------------------------------------------------------------------
_patient_db: Dict[str, Patient] = {
    "P001": Patient(
        code="P001",
        name="John Doe",
        age=34,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, medication",
    ),
    "P002": Patient(
        code="P002",
        name="Jane Smith",
        age=28,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler therapy",
    ),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_patient(patient_code: str) -> Patient:
    """Retrieve a patient from the repository, raising if not found."""
    try:
        return _patient_db[patient_code]
    except KeyError as exc:
        raise ValueError(f"Patient with code '{patient_code}' not found.") from exc


def _prepare_template_context(patient: Patient) -> Dict[str, str]:
    """
    Prepare a context dictionary for template rendering.
    Only non‑sensitive fields are included; attempts to access
    sensitive data will raise an exception.
    """
    context = {
        "patient.name": patient.name,
        "patient.age": str(patient.age),
        "patient.gender": patient.gender,
    }
    return context


def _render_template(template: str, context: Dict[str, str]) -> str:
    """
    Render the template by replacing placeholders of the form
    {patient.field} with their corresponding values from context.
    """
    # Find all placeholders
    placeholder_pattern = re.compile(r"\{([^}]+)\}")

    def replace(match: re.Match) -> str:
        key = match.group(1).strip()
        if key not in context:
            # Disallow accessing sensitive or unknown fields
            raise ValueError(f"Attempted to access disallowed or unknown field '{key}'.")
        return context[key]

    try:
        return placeholder_pattern.sub(replace, template)
    except ValueError as exc:
        raise  # propagate the error


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def create_person_report(patient_code: str, report_template: str) -> str:
    """
    Generate a non‑sensitive patient report based on the supplied template.

    Parameters
    ----------
    patient_code : str
        The unique identifier for a patient.
    report_template : str
        A template string containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The rendered report string.

    Raises
    ------
    ValueError
        If the patient does not exist or if the template tries to access
        sensitive data (diagnosis, treatment_plan) or an unknown field.
    """
    patient = _get_patient(patient_code)
    context = _prepare_template_context(patient)
    return _render_template(report_template, context)


# ----------------------------------------------------------------------
# Example usage (for testing purposes)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}"
    )
    print(create_person_report("P001", template))