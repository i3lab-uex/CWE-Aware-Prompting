import re
from dataclasses import dataclass, field
from typing import Dict

# -------------------------------------------------------------
# 1. Patient model (simplified)
# -------------------------------------------------------------
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str = field(repr=False)          # sensitive data
    treatment_plan: str = field(repr=False)     # sensitive data


# -------------------------------------------------------------
# 2. In‑memory patient store (for demo purposes)
# -------------------------------------------------------------
_PATIENT_STORE: Dict[str, Patient] = {
    "p001": Patient(
        patient_id="p001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "p002": Patient(
        patient_id="p002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler B, Regular check‑ups"
    ),
}


# -------------------------------------------------------------
# 3. Whitelist of safe attributes that can be exposed
# -------------------------------------------------------------
_SAFE_ATTRIBUTES = {"name", "age", "gender"}


# -------------------------------------------------------------
# 4. Build patient report
# -------------------------------------------------------------
def build_patient_report(patient_identifier: str, template_string: str) -> str:
    """
    Build a patient report by substituting placeholders in the template
    with actual patient data. Only safe attributes are allowed to be
    accessed; attempts to reference restricted fields raise ValueError.

    Args:
        patient_identifier (str): Unique patient ID.
        template_string (str): Template containing placeholders like
                               '{patient.name}'.

    Returns:
        str: The filled template string.

    Raises:
        ValueError: If patient ID is unknown or if the template tries
                    to access restricted data.
    """
    # 1. Retrieve patient
    patient = _PATIENT_STORE.get(patient_identifier)
    if not patient:
        raise ValueError(f"Invalid patient ID: {patient_identifier}")

    # 2. Find all placeholders of the form {patient.<attr>}
    pattern = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = pattern.findall(template_string)

    # 3. Validate and collect replacements
    replacements: Dict[str, str] = {}
    for attr in placeholders:
        if attr not in _SAFE_ATTRIBUTES:
            raise ValueError(f"Access to restricted attribute '{attr}' is denied")
        # Retrieve value via getattr
        value = getattr(patient, attr)
        replacements[f"patient.{attr}"] = str(value)

    # 4. Perform safe substitution
    def _safe_sub(match):
        key = match.group(0)[1:-1]  # remove braces
        return replacements.get(key, match.group(0))

    result = re.sub(r"\{patient\.[a-zA-Z_][a-zA-Z0-9_]*\}", _safe_sub, template_string)
    return result


# -------------------------------------------------------------
# 5. Example usage (uncomment to test)
# -------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Patient {patient.name} (Age: {patient.age}) is a {patient.gender}."
#     print(build_patient_report("p001", tmpl))