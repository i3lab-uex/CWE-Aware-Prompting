import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Mock patient database and data model
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class Patient:
    """Represents a patient in the system."""
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Restricted medical data
    treatment_plan: str     # Restricted medical data


# In a real system this would be replaced with database access.
PATIENT_DB: Dict[str, Patient] = {
    "p001": Patient(
        id="p001",
        name="Alice Smith",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Medication A, lifestyle changes"
    ),
    "p002": Patient(
        id="p002",
        name="Bob Johnson",
        age=45,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy, diet plan"
    ),
}


# ----------------------------------------------------------------------
# Core functionality
# ----------------------------------------------------------------------


def create_patient_report(id: str, report_template: str) -> str:
    """
    Create a patient report by filling in the provided template with
    patient data.

    Parameters
    ----------
    id : str
        Unique identifier of the patient.
    report_template : str
        Template string containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The template with patient data substituted.

    Raises
    ------
    ValueError
        If the patient ID is unknown or if a restricted attribute is
        accessed in the template.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve patient data
    # ------------------------------------------------------------------
    patient = PATIENT_DB.get(id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {id}")

    # ------------------------------------------------------------------
    # 2. Define allowed (non‑restricted) attributes
    # ------------------------------------------------------------------
    ALLOWED_ATTRS = {"name", "age", "gender"}

    # Build a mapping of allowed attributes
    patient_data = {
        f"patient.{attr}": getattr(patient, attr)
        for attr in ALLOWED_ATTRS
    }

    # ------------------------------------------------------------------
    # 3. Find all placeholders in the template
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders = placeholder_pattern.findall(report_template)

    # ------------------------------------------------------------------
    # 4. Validate and replace each placeholder
    # ------------------------------------------------------------------
    for ph in placeholders:
        if not ph.startswith("patient."):
            raise ValueError(f"Unsupported placeholder: {{{ph}}}")

        if ph not in patient_data:
            # Attempt to access restricted data
            raise ValueError(
                f"Access to restricted attribute '{ph.split('.', 1)[1]}' is not allowed"
            )

    # ------------------------------------------------------------------
    # 5. Perform safe substitution
    # ------------------------------------------------------------------
    def _replacement(match: re.Match) -> str:
        key = match.group(1)
        return str(patient_data[key])

    result = placeholder_pattern.sub(_replacement, report_template)

    return result


# ----------------------------------------------------------------------
# Example usage (for demonstration; remove or comment out in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(create_patient_report("p001", template))