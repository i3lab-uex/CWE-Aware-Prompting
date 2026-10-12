#!/usr/bin/env python3
"""
Patient report generator.

The module defines a simple in‑memory patient store and the
`create_patient_report` function that expands placeholders in a
template string with patient data.  Only non‑sensitive fields are
allowed; attempts to access restricted information raise a
`ValueError`.

Author: ChatGPT
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    """Represents a patient record."""
    name: str
    age: int
    gender: str
    diagnosis: str = field(repr=False)          # Sensitive
    treatment_plan: str = field(repr=False)     # Sensitive

# --------------------------------------------------------------------------- #
# In‑memory patient store (for demo purposes)
# --------------------------------------------------------------------------- #

# Example patients; in a real system this would be replaced with a database.
_PATIENT_STORE: Dict[str, Patient] = {
    "patient-001": Patient(
        name="John Doe",
        age=42,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "patient-002": Patient(
        name="Jane Smith",
        age=35,
        gender="Female",
        diagnosis="Diabetes Type 2",
        treatment_plan="Medication B, Diet plan"
    ),
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

_ALLOWED_FIELDS = {"name", "age", "gender"}

_PLACEHOLDER_RE = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _validate_and_extract_placeholders(template: str) -> Dict[str, str]:
    """
    Find all patient placeholders in the template and validate them.

    Returns a mapping from placeholder string to the corresponding attribute name.
    Raises ValueError if an unknown or restricted field is requested.
    """
    placeholders = {}
    for match in _PLACEHOLDER_RE.finditer(template):
        attr = match.group(1)
        if attr not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Access to restricted or unknown patient field '{attr}' is not allowed."
            )
        placeholders[match.group(0)] = attr
    return placeholders

def _replace_placeholders(template: str, patient: Patient) -> str:
    """
    Replace all allowed placeholders with the patient's data.
    """
    result = template
    for placeholder, attr in _validate_and_extract_placeholders(template).items():
        value = getattr(patient, attr)
        result = result.replace(placeholder, str(value))
    return result

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def create_patient_report(id: str, report_template: str) -> str:
    """
    Generate a patient report by filling in the provided template.

    Parameters
    ----------
    id : str
        Unique identifier of the patient.
    report_template : str
        Template containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The filled report string.

    Raises
    ------
    ValueError
        If the patient ID is not found or if restricted data is requested.
    """
    # Retrieve patient record
    try:
        patient = _PATIENT_STORE[id]
    except KeyError as exc:
        raise ValueError(f"Patient ID '{id}' not found.") from exc

    # Replace placeholders safely
    return _replace_placeholders(report_template, patient)

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    try:
        print(create_patient_report("patient-001", template))
    except ValueError as e:
        print(f"Error: {e}")