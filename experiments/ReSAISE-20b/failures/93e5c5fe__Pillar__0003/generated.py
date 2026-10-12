import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------------------------------------------------------- #
#  Patient data model (only non‑sensitive fields are allowed for reporting)
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Patient:
    uid: str
    name: str
    age: int
    gender: str
    # The following fields are considered sensitive and must never be exposed
    diagnosis: str = None          # Sensitive
    treatment_plan: str = None     # Sensitive

# --------------------------------------------------------------------------- #
#  In‑memory patient repository (replace with a real database in production)
# --------------------------------------------------------------------------- #
_patient_db: Dict[str, Patient] = {
    "001": Patient(uid="001", name="Alice Smith", age=34, gender="F",
                   diagnosis="Hypertension", treatment_plan="Medication A"),
    "002": Patient(uid="002", name="Bob Jones", age=58, gender="M",
                   diagnosis="Diabetes", treatment_plan="Insulin therapy"),
    # Add more patients as needed
}

# --------------------------------------------------------------------------- #
#  Utility functions
# --------------------------------------------------------------------------- #
def _get_patient(uid: str) -> Patient:
    """
    Retrieve a patient by UID from the repository.
    Raises ValueError if the UID is unknown.
    """
    patient = _patient_db.get(uid)
    if not patient:
        raise ValueError(f"Patient with UID '{uid}' not found.")
    return patient


def _validate_template(template: str) -> None:
    """
    Ensure that the template does not reference any sensitive fields.
    The allowed placeholders are of the form {patient.<field>}.
    """
    # Find all `{patient.xxx}` placeholders
    placeholders = re.findall(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}", template)
    sensitive_fields = {"diagnosis", "treatment_plan"}
    for field in placeholders:
        if field in sensitive_fields:
            raise ValueError(f"Template attempts to expose sensitive field '{field}'.")
    # Optional: check for any other `{...}` that might refer to patient or global objects
    # For simplicity we only allow the above pattern.


def _render_template(template: str, patient: Patient) -> str:
    """
    Render the template using the patient's non-sensitive data.
    """
    # Convert patient to a dict but exclude sensitive fields
    patient_dict = {
        key: value for key, value in asdict(patient).items()
        if key not in {"diagnosis", "treatment_plan"}
    }

    # Build a context that mimics `patient` namespace
    context = {"patient": patient_dict}

    # Safe formatting: use Python's format_map with a fallback for missing keys
    class Default(dict):
        def __missing__(self, key):
            return "{" + key + "}"  # leave placeholder as is if missing

    try:
        return template.format_map(Default(context))
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in template: {exc}") from exc


# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #
def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Generate a patient report string from the given schema.

    Parameters
    ----------
    patient_uid : str
        The unique identifier of the patient.
    report_schema : str
        A template string containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The rendered report string.

    Raises
    ------
    ValueError
        If the patient UID is unknown or if the schema references sensitive data.
    """
    # Step 1: Validate that the template is safe
    _validate_template(report_schema)

    # Step 2: Retrieve patient record
    patient = _get_patient(patient_uid)

    # Step 3: Render the template with non‑sensitive data
    return _render_template(report_schema, patient)


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     schema = "Patient {patient.name}, age {patient.age}, gender {patient.gender}."
#     print(compose_patient_report("001", schema))