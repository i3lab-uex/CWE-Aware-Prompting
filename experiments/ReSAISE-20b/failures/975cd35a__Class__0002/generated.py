import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------------- #
#  Data model and mock storage                                              #
# --------------------------------------------------------------------------- #

@dataclass
class Patient:
    """Represents a patient in the system."""
    identifier: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Restricted medical data
    treatment_plan: str     # Restricted medical data


# Mock patient database (identifier -> Patient)
PATIENT_DB: Dict[str, Patient] = {
    "patient_001": Patient(
        identifier="patient_001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lisinopril 10mg daily"
    ),
    "patient_002": Patient(
        identifier="patient_002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Albuterol inhaler as needed"
    ),
}


# --------------------------------------------------------------------------- #
#  Utility functions                                                        #
# --------------------------------------------------------------------------- #

def _get_patient(patient_identifier: str) -> Patient:
    """
    Retrieve a patient from the mock database.

    Raises:
        ValueError: If the patient identifier is not found.
    """
    patient = PATIENT_DB.get(patient_identifier)
    if patient is None:
        raise ValueError(f"Patient ID '{patient_identifier}' not found.")
    return patient


def _extract_placeholders(template: str) -> set:
    """
    Extract all placeholders of the form {patient.<field>} from the template.

    Returns:
        A set of field names (e.g., {'name', 'age'}).
    """
    pattern = r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}"
    return set(re.findall(pattern, template))


# --------------------------------------------------------------------------- #
#  Core function                                                            #
# --------------------------------------------------------------------------- #

def build_patient_report(patient_identifier: str, template_string: str) -> str:
    """
    Build a patient report by filling in placeholders with patient data.

    Parameters
    ----------
    patient_identifier : str
        Unique identifier of the patient.
    template_string : str
        Template containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if restricted data is requested.
    """
    # Retrieve patient
    patient = _get_patient(patient_identifier)

    # Define which fields are allowed for public reporting
    ALLOWED_FIELDS = {"name", "age", "gender"}

    # Find placeholders in the template
    placeholders = _extract_placeholders(template_string)

    # Check for restricted fields
    restricted_requested = placeholders - ALLOWED_FIELDS
    if restricted_requested:
        raise ValueError(
            f"Access to restricted patient data attempted: {', '.join(sorted(restricted_requested))}"
        )

    # Prepare a mapping for formatting
    data_map = {field: getattr(patient, field) for field in placeholders}

    try:
        report = template_string.format(**data_map)
    except KeyError as e:
        # This should not happen because we only use placeholders that exist
        raise ValueError(f"Missing data for placeholder: {e.args[0]}") from e

    return report


# --------------------------------------------------------------------------- #
#  Example usage (for demonstration only, remove in production)             #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(build_patient_report("patient_001", tmpl))

    # The following will raise an exception because 'diagnosis' is restricted
    try:
        tmpl_restricted = "Diagnosis: {patient.diagnosis}"
        print(build_patient_report("patient_001", tmpl_restricted))
    except ValueError as exc:
        print(f"Error: {exc}")