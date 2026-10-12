import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Domain model
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    uid: str
    name: str
    age: int
    gender: str
    # Sensitive fields are deliberately excluded from the public API
    _diagnosis: str = field(repr=False, compare=False)
    _treatment_plan: str = field(repr=False, compare=False)

    # Public getters for non‑sensitive data only
    @property
    def diagnosis(self) -> str:  # pragma: no cover
        return self._diagnosis

    @property
    def treatment_plan(self) -> str:  # pragma: no cover
        return self._treatment_plan


# ------------------------------------------------------------------
# In‑memory patient repository (mocked for this example)
# ------------------------------------------------------------------
_PATIENT_DB: Dict[str, Patient] = {
    "p001": Patient(
        uid="p001",
        name="Alice Smith",
        age=34,
        gender="F",
        _diagnosis="Hypertension",
        _treatment_plan="Medication A, lifestyle changes"
    ),
    "p002": Patient(
        uid="p002",
        name="Bob Jones",
        age=58,
        gender="M",
        _diagnosis="Diabetes",
        _treatment_plan="Insulin therapy"
    ),
}


# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
_PLACEHOLDER_RE = re.compile(r"\{([^\}]+)\}")

def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference any sensitive fields.
    Raises ValueError if it does.
    """
    for match in _PLACEHOLDER_RE.finditer(template):
        field_path = match.group(1).strip()
        # Only allow 'patient.<field>' pattern
        if not field_path.startswith("patient."):
            raise ValueError(f"Unsupported placeholder '{field_path}'")
        field_name = field_path.split(".", 1)[1]
        if field_name in {"diagnosis", "treatment_plan"}:
            raise ValueError(f"Access to sensitive field '{field_name}' is forbidden")


def _render_template(template: str, patient: Patient) -> str:
    """
    Replace placeholders with actual patient data.
    Assumes the template has already been validated.
    """
    def repl(match):
        field_path = match.group(1).strip()
        _, attr_name = field_path.split(".", 1)
        return str(getattr(patient, attr_name))

    return _PLACEHOLDER_RE.sub(repl, template)


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------
def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Generate a patient report string based on the supplied schema.

    Parameters
    ----------
    patient_uid : str
        Unique identifier of the patient.
    report_schema : str
        Template string containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient UID is unknown or if the schema attempts to access a
        sensitive field.
    """
    # 1. Retrieve patient
    patient = _PATIENT_DB.get(patient_uid)
    if not patient:
        raise ValueError(f"Patient with UID '{patient_uid}' not found")

    # 2. Validate template for sensitive fields
    _validate_template(report_schema)

    # 3. Render the final report
    return _render_template(report_schema, patient)


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = "Patient: {patient.name}, Age: {patient.age}, Gender: {patient.gender}"
    print(compose_patient_report("p001", template))