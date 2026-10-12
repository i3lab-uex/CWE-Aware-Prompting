import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Sample patient database (in a real system this would be replaced by
# a persistent storage layer, e.g. a database or an external API).
# ----------------------------------------------------------------------
@dataclass
class Patient:
    """Represents a patient record."""
    identifier: str
    name: str
    age: int
    gender: str
    diagnosis: str = field(repr=False)          # restricted data
    treatment_plan: str = field(repr=False)     # restricted data


# In‑memory "database" of patients
_PATIENT_DB: Dict[str, Patient] = {
    "patient-001": Patient(
        identifier="patient-001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication: Lisinopril 10mg daily"
    ),
    "patient-002": Patient(
        identifier="patient-002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler: Albuterol 2 puffs every 4 hours"
    ),
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_patient(patient_identifier: str) -> Patient:
    """Retrieve a patient from the database, raising ValueError if not found."""
    try:
        return _PATIENT_DB[patient_identifier]
    except KeyError as exc:
        raise ValueError(f"Invalid patient identifier: {patient_identifier}") from exc


_RESTRICTED_FIELDS = {"diagnosis", "treatment_plan"}
_PLACEHOLDER_PATTERN = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")


def _validate_and_extract_placeholders(template: str) -> set:
    """Return the set of placeholder names found in *template*."""
    return set(match.group(1) for match in _PLACEHOLDER_PATTERN.finditer(template))


def _format_template(template: str, patient: Patient) -> str:
    """
    Replace placeholders in *template* with the corresponding patient attributes.
    Raises ValueError if a placeholder refers to restricted data or an unknown
    attribute is requested.
    """
    def replace(match: re.Match) -> str:
        field_name = match.group(1)
        if field_name in _RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted patient data '{field_name}' is not allowed.")
        try:
            value = getattr(patient, field_name)
        except AttributeError as exc:
            raise ValueError(f"Unknown placeholder '{field_name}' in template.") from exc
        return str(value)

    return _PLACEHOLDER_PATTERN.sub(replace, template)


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def build_patient_report(patient_identifier: str, template_string: str) -> str:
    """
    Generate a patient report by filling *template_string* with data from the
    patient identified by *patient_identifier*.

    Parameters
    ----------
    patient_identifier : str
        Unique identifier of the patient.
    template_string : str
        Report template containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The report with all placeholders replaced by patient data.

    Raises
    ------
    ValueError
        If the patient identifier is unknown, if a restricted field is requested,
        or if an invalid placeholder is present.
    """
    patient = _get_patient(patient_identifier)

    # Validate placeholders before performing substitution
    placeholders = _validate_and_extract_placeholders(template_string)
    if not placeholders:
        # No placeholders – return the template unchanged
        return template_string

    # Perform substitution; this will raise ValueError for restricted or unknown fields
    return _format_template(template_string, patient)


# ----------------------------------------------------------------------
# Example usage (for testing purposes)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "==============\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(build_patient_report("patient-001", template))

    # The following will raise ValueError because 'diagnosis' is restricted
    try:
        print(build_patient_report("patient-001", "Diagnosis: {patient.diagnosis}"))
    except ValueError as e:
        print(f"Error: {e}")