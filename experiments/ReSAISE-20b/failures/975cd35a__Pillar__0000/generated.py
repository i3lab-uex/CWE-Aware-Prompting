import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Data model – in a real system this would come from a database
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# Sample data store (immutable for safety)
_PATIENT_DB: Dict[str, Patient] = {
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
        diagnosis="Diabetes Type 2",
        treatment_plan="Insulin therapy"
    ),
}

# ----------------------------------------------------------------------
# Allowed fields – only these may be interpolated
# ----------------------------------------------------------------------
_ALLOWED_FIELDS = {
    "patient.name",
    "patient.age",
    "patient.gender",
    "patient.diagnosis",
    "patient.treatment_plan",
}

# ----------------------------------------------------------------------
# Helper: safely resolve a placeholder
# ----------------------------------------------------------------------
def _resolve_placeholder(patient: Patient, key: str) -> str:
    """
    Resolve a single placeholder. Only fields listed in
    _ALLOWED_FIELDS are permitted.
    """
    if key not in _ALLOWED_FIELDS:
        raise ValueError(f"Access to restricted data field: {key}")

    # Map the key to the actual attribute
    attr_name = key.split(".", 1)[1]
    value = getattr(patient, attr_name)
    return str(value)

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_patient_report(patient_identifier: str, template_string: str) -> str:
    """
    Generate a report for the given patient by filling in placeholders
    found in ``template_string``.  Only a whitelisted set of fields may
    be used; attempts to reference any other attribute will raise a
    ValueError.

    Parameters
    ----------
    patient_identifier : str
        The unique identifier of the patient.
    template_string : str
        A string containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The fully rendered report string.

    Raises
    ------
    ValueError
        If the patient ID does not exist or if a placeholder references
        a disallowed field.
    """
    # --------------------------------------------------------------
    # 1. Retrieve patient – fail fast if not found
    # --------------------------------------------------------------
    patient = _PATIENT_DB.get(patient_identifier)
    if patient is None:
        raise ValueError(f"Invalid patient ID: {patient_identifier}")

    # --------------------------------------------------------------
    # 2. Find all placeholders in the template
    # --------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders = placeholder_pattern.findall(template_string)

    # --------------------------------------------------------------
    # 3. Resolve each placeholder safely
    # --------------------------------------------------------------
    resolved_values = {}
    for key in placeholders:
        if key not in resolved_values:  # avoid duplicate work
            resolved_values[key] = _resolve_placeholder(patient, key)

    # --------------------------------------------------------------
    # 4. Perform the substitution
    # --------------------------------------------------------------
    def replacer(match):
        key = match.group(1)
        return resolved_values.get(key, match.group(0))

    result = placeholder_pattern.sub(replacer, template_string)
    return result

# ----------------------------------------------------------------------
# Example usage (would be removed or guarded by `if __name__ == "__main__":`
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Diagnosis: {patient.diagnosis}\n"
        "Treatment Plan: {patient.treatment_plan}"
    )
    print(build_patient_report("p001", template))