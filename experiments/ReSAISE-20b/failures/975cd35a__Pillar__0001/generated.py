import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
#  Data model
# ------------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    """Represents a patient record."""
    identifier: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive data
    treatment_plan: str     # Sensitive data


# ------------------------------------------------------------------
#  In‑memory patient store (for demonstration purposes)
# ------------------------------------------------------------------

_PATIENT_STORE: Dict[str, Patient] = {
    "P001": Patient(
        identifier="P001",
        name="Alice Smith",
        age=30,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Low-sodium diet and medication A",
    ),
    "P002": Patient(
        identifier="P002",
        name="Bob Johnson",
        age=45,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy and diet B",
    ),
}


# ------------------------------------------------------------------
#  Utility helpers
# ------------------------------------------------------------------

def _get_patient(patient_id: str) -> Patient:
    """
    Retrieve a patient by ID.

    Raises ValueError if the ID is not found.
    """
    try:
        return _PATIENT_STORE[patient_id]
    except KeyError as exc:
        raise ValueError(f"Patient ID '{patient_id}' not found.") from exc


# ------------------------------------------------------------------
#  Main function
# ------------------------------------------------------------------

def build_patient_report(patient_identifier: str, template_string: str) -> str:
    """
    Build a report for the given patient by filling in placeholders.

    Parameters
    ----------
    patient_identifier : str
        Unique identifier for the patient.
    template_string : str
        Template containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The report with placeholders replaced by actual patient data.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if the template attempts to access
        restricted medical data (diagnosis, treatment_plan).
    """
    # Retrieve patient record
    patient = _get_patient(patient_identifier)

    # Identify placeholders in the template
    placeholder_pattern = re.compile(r"\{patient\.([a-zA-Z_]+)\}")
    placeholders = placeholder_pattern.findall(template_string)

    # Determine which attributes are allowed
    allowed_attrs = {"name", "age", "gender"}
    restricted_attrs = {"diagnosis", "treatment_plan"}

    # Check for restricted data access
    if any(attr in restricted_attrs for attr in placeholders):
        raise ValueError("Access to restricted medical data is not allowed.")

    # Validate that all placeholders correspond to actual attributes
    for attr in placeholders:
        if attr not in allowed_attrs:
            raise ValueError(f"Unknown placeholder '{{patient.{attr}}}' in template.")

    # Build a mapping for formatting
    mapping = {f"patient.{attr}": getattr(patient, attr) for attr in placeholders}

    # Perform safe replacement
    def replacer(match: re.Match) -> str:
        key = match.group(0)[1:-1]  # strip braces
        return str(mapping[key])

    result = placeholder_pattern.sub(replacer, template_string)

    return result


# ------------------------------------------------------------------
#  Example usage (uncomment to test)
# ------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(build_patient_report("P001", template))