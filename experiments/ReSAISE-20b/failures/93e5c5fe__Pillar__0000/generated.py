import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------------------------------------------------------- #
#   Patient data model (non‑sensitive fields only)
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    uid: str
    name: str
    age: int
    gender: str

# --------------------------------------------------------------------------- #
#   In‑memory patient registry (simulating a database)
# --------------------------------------------------------------------------- #

# For demonstration purposes, the registry is pre‑populated.
_PATIENT_REGISTRY: Dict[str, Patient] = {
    "12345": Patient(uid="12345", name="Alice Smith", age=29, gender="F"),
    "67890": Patient(uid="67890", name="Bob Johnson", age=42, gender="M"),
}

# --------------------------------------------------------------------------- #
#   Utility functions
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}

def _get_patient(uid: str) -> Patient:
    """
    Retrieve a patient from the registry.
    Raises ValueError if the uid is not found.
    """
    try:
        return _PATIENT_REGISTRY[uid]
    except KeyError as exc:
        raise ValueError(f"Patient with UID '{uid}' not found.") from exc

def _prepare_template_context(patient: Patient) -> Dict[str, str]:
    """
    Convert a Patient instance into a mapping suitable for template substitution.
    Only non‑sensitive fields are exposed. Any attempt to access a sensitive
    field will raise ValueError.
    """
    context = asdict(patient)
    # Remove any sensitive keys if they exist (safety net)
    for key in _SENSITIVE_FIELDS:
        context.pop(key, None)

    # Ensure all values are strings for formatting
    return {k: str(v) for k, v in context.items()}

def _validate_template(report_schema: str):
    """
    Ensure that the template does not reference any sensitive fields.
    The regex captures words inside braces. If a sensitive field name
    appears, raise ValueError.
    """
    placeholders = re.findall(r"{([^}]+)}", report_schema)
    for field in placeholders:
        # Field names may be prefixed (e.g., patient.name). We only check the last part.
        field_name = field.split(".")[-1]
        if field_name in _SENSITIVE_FIELDS:
            raise ValueError(f"Template contains forbidden sensitive field '{field}'.")
    return

# --------------------------------------------------------------------------- #
#   Main function
# --------------------------------------------------------------------------- #

def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Compose a patient report using the provided template.

    Parameters
    ----------
    patient_uid : str
        The unique identifier of the patient.
    report_schema : str
        A string template containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The formatted report string containing only non‑sensitive patient data.

    Raises
    ------
    ValueError
        If the patient UID does not exist or if the template attempts to
        access sensitive information.
    """
    # Validate that we are not leaking resources: in this context, no external
    # resource is opened so we only ensure that the function behaves deterministically.
    _validate_template(report_schema)

    patient = _get_patient(patient_uid)
    context = _prepare_template_context(patient)

    # The template may use a namespace prefix like 'patient.name'.
    # We replace the prefix with an empty string for formatting.
    def _replace_namespace(match):
        full = match.group(0)
        # Strip 'patient.' prefix if present
        key = full[1:-1]  # remove braces
        key_no_ns = key.split(".")[-1]
        return context.get(key_no_ns, f"<missing:{key}>")

    # Use regex substitution to safely replace placeholders
    pattern = re.compile(r"{[^}]+}")
    safe_report = pattern.sub(_replace_namespace, report_schema)

    return safe_report

# --------------------------------------------------------------------------- #
#   Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     template = "Patient: {patient.name}, Age: {patient.age}, Gender: {patient.gender}"
#     print(compose_patient_report("12345", template))