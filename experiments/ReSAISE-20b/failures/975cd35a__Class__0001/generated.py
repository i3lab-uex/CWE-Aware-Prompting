#!/usr/bin/env python3
"""
Patient report builder.

This module defines a simple in‑memory patient store and the function
`build_patient_report`.  The function substitutes placeholders in a
template string with attributes from the patient record, but it
rejects access to sensitive fields such as `diagnosis` and
`treatment_plan`.  If an unknown patient ID is supplied or a
restricted field is requested, a `ValueError` is raised.

The implementation intentionally keeps the data store minimal and
does not use any external libraries beyond the standard library.
"""

import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# Patient data model
# --------------------------------------------------------------------

@dataclass
class Patient:
    """Represents a patient record."""
    name: str
    age: int
    gender: str
    diagnosis: str = field(repr=False)          # sensitive
    treatment_plan: str = field(repr=False)     # sensitive

# --------------------------------------------------------------------
# In‑memory patient database
# --------------------------------------------------------------------

# Example data – in a real system this would be loaded from a secure DB.
PATIENT_DB: Dict[str, Patient] = {
    "patient_001": Patient(
        name="Alice Smith",
        age=34,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Medication A, lifestyle changes"
    ),
    "patient_002": Patient(
        name="Bob Jones",
        age=45,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Medication B, diet plan"
    ),
}

# --------------------------------------------------------------------
# Report building logic
# --------------------------------------------------------------------

PLACEHOLDER_PATTERN = re.compile(r"\{(?P<obj>\w+)\.(?P<attr>\w+)\}")

# Attributes that are considered sensitive and must not be exposed
RESTRICTED_ATTRIBUTES = {"diagnosis", "treatment_plan"}

def _validate_patient(patient_id: str) -> Patient:
    """Retrieve patient or raise ValueError."""
    try:
        return PATIENT_DB[patient_id]
    except KeyError as exc:
        raise ValueError(f"Invalid patient identifier: {patient_id}") from exc

def _extract_placeholders(template: str):
    """Yield (obj, attr) tuples found in the template."""
    for match in PLACEHOLDER_PATTERN.finditer(template):
        yield match.group("obj"), match.group("attr")

def build_patient_report(patient_identifier: str, template_string: str) -> str:
    """
    Build a report string for the given patient by replacing placeholders.

    Parameters
    ----------
    patient_identifier : str
        The unique identifier of the patient.
    template_string : str
        A string containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The template with placeholders replaced by patient data.

    Raises
    ------
    ValueError
        If the patient ID is unknown or if a restricted field is requested.
    """
    # Retrieve patient data
    patient = _validate_patient(patient_identifier)

    # Build a mapping of allowed attributes
    data_map = {
        "name": patient.name,
        "age": str(patient.age),
        "gender": patient.gender,
    }

    # Check placeholders for restricted fields
    for obj, attr in _extract_placeholders(template_string):
        if obj != "patient":
            raise ValueError(f"Unsupported placeholder object: {obj}")
        if attr in RESTRICTED_ATTRIBUTES:
            raise ValueError(f"Access to restricted attribute '{attr}' is not allowed")

        if attr not in data_map:
            raise ValueError(f"Unknown attribute '{attr}' requested in template")

    # Perform the substitution
    def replacer(match):
        attr = match.group("attr")
        return data_map[attr]

    result = PLACEHOLDER_PATTERN.sub(replacer, template_string)
    return result

# --------------------------------------------------------------------
# Example usage
# --------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = "Patient {patient.name}, Age: {patient.age}, Gender: {patient.gender}."
    try:
        print(build_patient_report("patient_001", tmpl))
    except ValueError as e:
        print(f"Error: {e}")