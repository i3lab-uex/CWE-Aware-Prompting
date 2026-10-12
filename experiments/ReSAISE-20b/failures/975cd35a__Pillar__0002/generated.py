import re
from typing import Dict

# ------------------------------
# Simple in‑memory patient store
# ------------------------------

class Patient:
    """
    Basic patient data structure.
    Only a subset of attributes is considered safe for reporting.
    """
    def __init__(self, patient_id: str,
                 name: str,
                 age: int,
                 gender: str,
                 diagnosis: str,
                 treatment_plan: str):
        self.id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        # The following attributes are considered *restricted* for general reports
        self._diagnosis = diagnosis          # Sensitive
        self._treatment_plan = treatment_plan  # Sensitive

    @property
    def diagnosis(self):
        raise AttributeError("Access to 'diagnosis' is restricted")

    @property
    def treatment_plan(self):
        raise AttributeError("Access to 'treatment_plan' is restricted")

    # Public getters for safe attributes
    @property
    def patient_name(self):
        return self.name

    @property
    def patient_age(self):
        return str(self.age)

    @property
    def patient_gender(self):
        return self.gender

# In‑memory database of patients (patient_id -> Patient instance)
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient("P001", "Alice Smith", 34, "F", "Hypertension", "Lifestyle changes"),
    "P002": Patient("P002", "Bob Jones", 45, "M", "Diabetes", "Insulin therapy"),
    # Add more patients as needed
}

# ------------------------------
# Report builder
# ------------------------------

PLACEHOLDER_PATTERN = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

# Map of allowed placeholder names to Patient attribute accessors
_ALLOWED_PLACEHOLDERS = {
    "name": lambda p: p.patient_name,
    "age": lambda p: p.patient_age,
    "gender": lambda p: p.patient_gender,
}

def _resolve_placeholder(patient: Patient, key: str) -> str:
    """
    Resolve a single placeholder against the patient object.
    Raises ValueError if the key is not allowed or patient access fails.
    """
    if key not in _ALLOWED_PLACEHOLDERS:
        raise ValueError(f"Unauthorized placeholder '{{patient.{key}}}'")
    try:
        return _ALLOWED_PLACEHOLDERS[key](patient)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to resolve placeholder '{{patient.{key}}}': {exc}") from exc

def build_patient_report(patient_identifier: str, template_string: str) -> str:
    """
    Build a patient report by replacing placeholders in the template with
    actual patient data.

    Parameters
    ----------
    patient_identifier : str
        Unique identifier for the patient.
    template_string : str
        Report template containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The populated report string.

    Raises
    ------
    ValueError
        If the patient ID is unknown or if a restricted attribute is accessed.
    """
    # Retrieve patient; enforce existence
    patient = _PATIENT_DB.get(patient_identifier)
    if patient is None:
        raise ValueError(f"Invalid patient identifier: {patient_identifier}")

    # Find all placeholders in the template
    matches = PLACEHOLDER_PATTERN.findall(template_string)

    # Build a mapping of placeholder to resolved value
    resolved = {}
    for key in set(matches):
        resolved[key] = _resolve_placeholder(patient, key)

    # Perform safe replacement
    def replace_match(match: re.Match) -> str:
        key = match.group(1)
        return resolved.get(key, match.group(0))

    result = PLACEHOLDER_PATTERN.sub(replace_match, template_string)
    return result

# ------------------------------
# Example usage (uncomment to test)
# ------------------------------

# if __name__ == "__main__":
#     tmpl = "Patient {patient.name} (Age: {patient.age}) is a {patient.gender}. "
#     print(build_patient_report("P001", tmpl))