#!/usr/bin/env python3
"""
A minimal implementation of a healthcare reporting system.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    """
    Immutable patient record.
    Only non‑sensitive fields are exposed for reporting.
    """
    code: str
    name: str
    age: int
    gender: str

    # Sensitive fields are deliberately omitted from the public interface.
    _diagnosis: str = field(repr=False, compare=False)
    _treatment_plan: str = field(repr=False, compare=False)

    @property
    def diagnosis(self) -> None:
        raise AttributeError("Access to 'diagnosis' is prohibited.")

    @property
    def treatment_plan(self) -> None:
        raise AttributeError("Access to 'treatment_plan' is prohibited.")


# --------------------------------------------------------------------------- #
# In‑memory patient store (simulating a database)
# --------------------------------------------------------------------------- #

class PatientRepository:
    """
    A very small repository that holds patient records.
    In a real system this would be backed by a database.
    """
    _store: Dict[str, Patient] = {}

    @classmethod
    def add_patient(cls, patient: Patient) -> None:
        cls._store[patient.code] = patient

    @classmethod
    def get_patient(cls, code: str) -> Patient:
        try:
            return cls._store[code]
        except KeyError as exc:
            raise ValueError(f"Patient with code '{code}' not found.") from exc


# --------------------------------------------------------------------------- #
# Report generation
# --------------------------------------------------------------------------- #

_PLACEHOLDER_REGEX = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

# Fields that are considered sensitive and must not appear in a report
_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}


def create_person_report(patient_code: str, report_template: str) -> str:
    """
    Generate a patient report from the provided template.

    Parameters
    ----------
    patient_code : str
        Identifier of the patient.
    report_template : str
        Template containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient does not exist or if the template contains a sensitive field.
    """
    # Validate placeholders for sensitivity
    placeholders = _PLACEHOLDER_REGEX.findall(report_template)
    if any(field in _SENSITIVE_FIELDS for field in placeholders):
        raise ValueError("Template contains sensitive patient data.")

    # Retrieve the patient
    patient = PatientRepository.get_patient(patient_code)

    # Build a mapping of allowed fields
    allowed_fields: Dict[str, Any] = {
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
    }

    # Perform safe formatting
    try:
        report = report_template.format(patient=allowed_fields)
    except KeyError as exc:
        raise ValueError(f"Template refers to unknown field: {exc}") from exc
    except Exception as exc:
        # Catch any other formatting errors
        raise ValueError(f"Error while formatting report: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create some patients
    PatientRepository.add_patient(
        Patient(
            code="P001",
            name="John Doe",
            age=45,
            gender="Male",
            _diagnosis="Hypertension",
            _treatment_plan="Medication A",
        )
    )

    PatientRepository.add_patient(
        Patient(
            code="P002",
            name="Jane Smith",
            age=30,
            gender="Female",
            _diagnosis="Asthma",
            _treatment_plan="Inhaler B",
        )
    )

    # Define a safe template
    tmpl = "Patient {patient.name} is {patient.age} years old and identifies as {patient.gender}."

    # Generate reports
    print(create_person_report("P001", tmpl))
    print(create_person_report("P002", tmpl))

    # Attempting to use a sensitive field triggers an error
    try:
        bad_tmpl = "Diagnosis: {patient.diagnosis}"
        create_person_report("P001", bad_tmpl)
    except ValueError as e:
        print(f"Caught error: {e}")