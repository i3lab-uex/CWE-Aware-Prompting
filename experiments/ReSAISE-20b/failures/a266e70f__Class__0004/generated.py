import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Data model – in a real system this would be backed by a database
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str
    # Fields that are considered sensitive and should not be exposed
    _sensitive_fields: set = field(default_factory=lambda: {"diagnosis", "treatment_plan"}, init=False, repr=False)

# In‑memory patient repository (replace with real persistence in production)
_patient_db: Dict[str, Patient] = {
    "p001": Patient(id="p001", name="Alice Smith", age=34, gender="F",
                    diagnosis="Hypertension", treatment_plan="Medication A"),
    "p002": Patient(id="p002", name="Bob Jones", age=58, gender="M",
                    diagnosis="Diabetes", treatment_plan="Insulin therapy"),
}


# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def _get_patient(id: str) -> Patient:
    """Retrieve a patient from the repository or raise ValueError."""
    if id not in _patient_db:
        raise ValueError(f"Invalid patient ID: {id}")
    return _patient_db[id]


def _extract_placeholder_name(placeholder: str) -> str:
    """Return the attribute name inside a placeholder like 'patient.name'."""
    parts = placeholder.split(".")
    if len(parts) != 2 or parts[0] != "patient":
        raise ValueError(f"Unsupported placeholder format: {{{placeholder}}}")
    return parts[1]


# ------------------------------------------------------------------
# Main API
# ------------------------------------------------------------------
def create_patient_report(id: str, report_template: str) -> str:
    """
    Generate a patient report by substituting placeholders in the template
    with data from the specified patient.

    Parameters
    ----------
    id : str
        Unique identifier of the patient.
    report_template : str
        Template string containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The report with all placeholders replaced by patient data.

    Raises
    ------
    ValueError
        If the patient ID is invalid or a restricted field is accessed.
    """
    # Retrieve patient data
    patient = _get_patient(id)

    # Regular expression to find all placeholders of the form {patient.xxx}
    placeholder_pattern = re.compile(r"\{([^\{\}]+)\}")

    def _replace(match):
        placeholder = match.group(1).strip()
        attr_name = _extract_placeholder_name(placeholder)

        # Check for restricted data
        if attr_name in patient._sensitive_fields:
            raise ValueError(f"Access to restricted field '{attr_name}' is not allowed.")

        # Retrieve the attribute value
        if not hasattr(patient, attr_name):
            raise ValueError(f"Unknown patient field: '{attr_name}'")

        return str(getattr(patient, attr_name))

    # Perform substitution
    try:
        report = placeholder_pattern.sub(_replace, report_template)
    except ValueError as exc:
        # Re‑raise to propagate error
        raise

    return report


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(create_patient_report("p001", template))