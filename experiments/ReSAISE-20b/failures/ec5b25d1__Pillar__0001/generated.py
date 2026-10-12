import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# 1. Domain model – Patient
# --------------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    """Immutable patient record containing non‑sensitive data."""
    code: str
    name: str
    age: int
    gender: str
    # Sensitive fields – not exposed through the reporting API
    _diagnosis: str = field(repr=False, compare=False)
    _treatment_plan: str = field(repr=False, compare=False)

# --------------------------------------------------------------------
# 2. In‑memory registry (simulating a data source)
# --------------------------------------------------------------------

# This would normally be replaced by a database or external service.
PATIENT_REGISTRY: Dict[str, Patient] = {
    "P001": Patient(
        code="P001",
        name="John Doe",
        age=42,
        gender="Male",
        _diagnosis="Hypertension",
        _treatment_plan="Medication A, Lifestyle changes"
    ),
    "P002": Patient(
        code="P002",
        name="Jane Smith",
        age=35,
        gender="Female",
        _diagnosis="Diabetes Type II",
        _treatment_plan="Insulin therapy"
    ),
}

# --------------------------------------------------------------------
# 3. Utility helpers
# --------------------------------------------------------------------

SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}

def _extract_placeholders(template: str) -> set:
    """
    Extract placeholders of the form {patient.<field>} from a template string.
    Returns a set of field names (without the 'patient.' prefix).
    """
    # Regex matches {patient.<identifier>}
    pattern = r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}"
    return set(re.findall(pattern, template))

def _patient_to_dict(patient: Patient) -> Dict[str, str]:
    """
    Convert a Patient instance to a dictionary suitable for string formatting.
    Only non‑sensitive attributes are exposed.
    """
    return {
        "name": patient.name,
        "age": str(patient.age),
        "gender": patient.gender,
    }

# --------------------------------------------------------------------
# 4. Main API
# --------------------------------------------------------------------

def create_person_report(patient_code: str, report_template: str) -> str:
    """
    Generate a patient report from the given template.

    Parameters
    ----------
    patient_code : str
        Unique identifier of the patient.
    report_template : str
        Template string containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        Formatted report string with non‑sensitive patient information.

    Raises
    ------
    ValueError
        If the patient is not found, or if the template attempts to access
        sensitive fields (diagnosis or treatment_plan).
    """
    # 1. Retrieve the patient record
    patient = PATIENT_REGISTRY.get(patient_code)
    if not patient:
        raise ValueError(f"Patient with code '{patient_code}' not found.")

    # 2. Parse placeholders
    placeholders = _extract_placeholders(report_template)

    # 3. Check for forbidden fields
    if placeholders & SENSITIVE_FIELDS:
        forbidden = ", ".join(placeholders & SENSITIVE_FIELDS)
        raise ValueError(
            f"Template attempts to access sensitive fields: {forbidden}"
        )

    # 4. Prepare data for formatting
    patient_dict = _patient_to_dict(patient)

    # 5. Replace placeholders using str.format
    try:
        report = report_template.format(patient=patient_dict)
    except KeyError as e:
        # A placeholder references a non‑existent attribute
        raise ValueError(f"Unknown field in template: {e.args[0]}") from e

    return report

# --------------------------------------------------------------------
# 5. Example usage (uncomment to test)
# --------------------------------------------------------------------

# if __name__ == "__main__":
#     tmpl = "Patient {patient.name}, Age: {patient.age}, Gender: {patient.gender}."
#     print(create_person_report("P001", tmpl))