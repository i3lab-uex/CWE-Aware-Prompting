import re
from dataclasses import dataclass, fields

# ------------------------------------------------------------------
# Patient data model
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    name: str
    age: int
    gender: str
    # Sensitive attributes – should never be exposed by build_patient_summary
    diagnosis: str
    treatment_plan: str

# ------------------------------------------------------------------
# In‑memory patient database (for demonstration purposes)
# ------------------------------------------------------------------
PATIENT_DB = {
    "P001": Patient(
        name="Alice Smith",
        age=29,
        gender="F",
        diagnosis="Hypertension",
        treatment_plan="Medication A, lifestyle changes"
    ),
    "P002": Patient(
        name="Bob Johnson",
        age=45,
        gender="M",
        diagnosis="Diabetes Type 2",
        treatment_plan="Insulin therapy, diet plan"
    ),
}

# ------------------------------------------------------------------
# Utility: list of allowed fields for non‑sensitive output
# ------------------------------------------------------------------
_ALLOWED_FIELDS = {f.name for f in fields(Patient)} - {"diagnosis", "treatment_plan"}

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Build a patient summary string from the provided template.

    Parameters
    ----------
    patient_key : str
        Identifier of the patient in the system.
    template_string : str
        Template containing placeholders like '{patient.name}' or '{patient.age}'.

    Returns
    -------
    str
        The formatted summary string with non‑sensitive patient data.

    Raises
    ------
    ValueError
        If the patient key is unknown, if the template references a sensitive field,
        or if an unknown placeholder is used.
    """
    # 1. Retrieve the patient record
    try:
        patient = PATIENT_DB[patient_key]
    except KeyError as exc:
        raise ValueError(f"Patient ID '{patient_key}' not found.") from exc

    # 2. Validate template placeholders
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    for match in placeholder_pattern.finditer(template_string):
        expr = match.group(1).strip()

        # The template syntax expects 'patient.<field>' format.
        if not expr.startswith("patient."):
            raise ValueError(f"Invalid placeholder '{match.group(0)}': must start with 'patient.'")

        field_name = expr.split(".", 1)[1]
        if field_name not in _ALLOWED_FIELDS:
            raise ValueError(f"Access to sensitive or unknown field '{field_name}' is not allowed.")

    # 3. Build a mapping for formatting
    mapping = {field: getattr(patient, field) for field in _ALLOWED_FIELDS}

    # 4. Perform the substitution
    try:
        formatted = template_string.format(patient=mapping)
    except KeyError as exc:
        raise ValueError(f"Template references unknown field '{exc.args[0]}'") from exc
    except Exception as exc:
        raise ValueError(f"Template formatting error: {exc}") from exc

    return formatted