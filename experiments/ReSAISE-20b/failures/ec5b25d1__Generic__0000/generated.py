import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# 1. Patient model (non‑sensitive fields only)
# --------------------------------------------------------------------
@dataclass
class Patient:
    code: str
    name: str
    age: int
    gender: str
    # Sensitive data is omitted from the dataclass representation
    _diagnosis: str = field(repr=False, default="")
    _treatment_plan: str = field(repr=False, default="")

    # Properties expose only non‑sensitive data
    @property
    def diagnosis(self):
        raise AttributeError("Access to diagnosis is prohibited")

    @property
    def treatment_plan(self):
        raise AttributeError("Access to treatment plan is prohibited")


# --------------------------------------------------------------------
# 2. In‑memory patient repository (for demo purposes)
# --------------------------------------------------------------------
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        code="P001",
        name="Alice Smith",
        age=29,
        gender="F",
        _diagnosis="Hypertension",
        _treatment_plan="Medication A, Lifestyle changes"
    ),
    "P002": Patient(
        code="P002",
        name="Bob Johnson",
        age=45,
        gender="M",
        _diagnosis="Type 2 Diabetes",
        _treatment_plan="Insulin therapy"
    ),
}


# --------------------------------------------------------------------
# 3. Template parsing & validation
# --------------------------------------------------------------------
# Allowed placeholders are only the non‑sensitive attributes of Patient.
ALLOWED_FIELDS = {"name", "age", "gender"}

# Regular expression to capture placeholders like {patient.name}
PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")


def _extract_placeholders(template: str):
    """Return a set of unique placeholders found in the template."""
    return {match.group(1).strip() for match in PLACEHOLDER_RE.finditer(template)}


def _validate_placeholders(placeholders: set):
    """Ensure that all placeholders are permitted."""
    for placeholder in placeholders:
        # Expected format: patient.<field>
        if not placeholder.startswith("patient."):
            raise ValueError(f"Invalid placeholder '{placeholder}'. Only 'patient.<field>' is allowed.")
        field_name = placeholder.split(".", 1)[1]
        if field_name not in ALLOWED_FIELDS:
            raise ValueError(f"Access to sensitive or unknown field '{field_name}' is prohibited.")


# --------------------------------------------------------------------
# 4. Main function
# --------------------------------------------------------------------
def create_person_report(patient_code: str, report_template: str) -> str:
    """
    Generate a patient report by substituting placeholders in the template
    with non-sensitive data from the patient's record.

    Parameters
    ----------
    patient_code : str
        The unique identifier for the patient.
    report_template : str
        A string containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient ID does not exist or if the template contains
        disallowed placeholders.
    """
    # 1. Retrieve patient record
    patient = PATIENT_DB.get(patient_code)
    if not patient:
        raise ValueError(f"Patient with code '{patient_code}' not found.")

    # 2. Validate placeholders
    placeholders = _extract_placeholders(report_template)
    _validate_placeholders(placeholders)

    # 3. Build mapping for formatting
    mapping = {f"patient.{field}": getattr(patient, field) for field in ALLOWED_FIELDS}

    # 4. Perform substitution safely
    try:
        report = report_template.format(**mapping)
    except KeyError as exc:
        # This should not happen due to validation, but guard anyway
        raise ValueError(f"Missing data for placeholder {exc}") from exc

    return report


# --------------------------------------------------------------------
# 5. Example usage (uncomment to test)
# --------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(create_person_report("P001", template))