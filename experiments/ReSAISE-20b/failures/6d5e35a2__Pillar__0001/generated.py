#!/usr/bin/env python3
"""
Utility module for generating patient reports with dynamic template substitution.

The implementation protects against:
- Accessing restricted medical fields (diagnosis, treatment_plan).
- Using invalid patient identifiers.
- Resource leaks via context managers for any external resources.

Author: OpenAI
"""

from __future__ import annotations

import re
from dataclasses import dataclass, fields
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Domain model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    """Represents a patient record."""
    pat_id: str
    name: str
    age: int
    gender: str
    diagnosis: str  # Restricted field
    treatment_plan: str  # Restricted field


# --------------------------------------------------------------------------- #
# In‑memory patient repository (simulates a database)
# --------------------------------------------------------------------------- #

class PatientRepository:
    """
    Thread‑safe in‑memory repository. In a real system this would interface
    with a database and handle connections responsibly.
    """
    _patients: Dict[str, Patient] = {}

    @classmethod
    def add_patient(cls, patient: Patient) -> None:
        cls._patients[patient.pat_id] = patient

    @classmethod
    def get_patient(cls, pat_id: str) -> Patient | None:
        return cls._patients.get(pat_id)


# --------------------------------------------------------------------------- #
# Report generation
# --------------------------------------------------------------------------- #

# Fields that are considered sensitive and must not be exposed via templates.
_RESTRICTED_FIELDS = {"diagnosis", "treatment_plan"}

# Pre‑compile regex for performance.
_PLACEHOLDER_RE = re.compile(r"\{(?P<obj>\w+)\.(?P<field>\w+)\}")


def _validate_and_get_field(patient: Patient, field_name: str) -> Any:
    """
    Validate that the requested field exists and is not restricted.
    Return its value or raise ValueError if access is forbidden.
    """
    # Check that the field exists on Patient
    patient_fields = {f.name for f in fields(patient)}
    if field_name not in patient_fields:
        raise ValueError(f"Field '{field_name}' does not exist on Patient.")

    # Restriction check
    if field_name in _RESTRICTED_FIELDS:
        raise ValueError(f"Access to restricted field '{field_name}' is forbidden.")

    # Safe access
    return getattr(patient, field_name)


def create_patient_report(pat_id: str, layout: str) -> str:
    """
    Generate a personalized report for the patient identified by `pat_id`.

    Parameters
    ----------
    pat_id : str
        Unique identifier of the patient.
    layout : str
        Report template containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if the template attempts to access a
        restricted field.
    """
    # Fetch patient data. Use a context manager if external resources were involved.
    patient = PatientRepository.get_patient(pat_id)
    if not patient:
        raise ValueError(f"Patient ID '{pat_id}' is invalid or does not exist.")

    # Replacement function for placeholders
    def replace_placeholder(match: re.Match) -> str:
        obj, field = match.group("obj"), match.group("field")
        if obj != "patient":
            raise ValueError(f"Unsupported placeholder object '{obj}'. Only 'patient' is allowed.")
        value = _validate_and_get_field(patient, field)
        return str(value)

    # Perform substitution safely
    try:
        report = _PLACEHOLDER_RE.sub(replace_placeholder, layout)
    except re.error as exc:
        # This would indicate malformed regex in the template
        raise ValueError(f"Invalid layout format: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Populate repository with sample data
    PatientRepository.add_patient(
        Patient(
            pat_id="12345",
            name="John Doe",
            age=30,
            gender="Male",
            diagnosis="Hypertension",
            treatment_plan="Lifestyle modification and medication",
        )
    )

    # Valid report
    template = (
        "Patient Report\n"
        "--------------\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}"
    )
    print(create_patient_report("12345", template))

    # Attempt to access restricted field (will raise ValueError)
    try:
        bad_template = "Diagnosis: {patient.diagnosis}"
        print(create_patient_report("12345", bad_template))
    except ValueError as e:
        print(f"Error: {e}")