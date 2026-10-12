#!/usr/bin/env python3
"""
A minimal patient reporting module.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    """Represents a patient record."""
    identifier: str
    name: str
    age: int
    gender: str
    diagnosis: str            # Sensitive / restricted field
    treatment_plan: str       # Sensitive / restricted field


# --------------------------------------------------------------------------- #
# In‑memory patient store (for demo purposes)
# --------------------------------------------------------------------------- #

_PATIENT_DB: Dict[str, Patient] = {
    "p001": Patient(
        identifier="p001",
        name="Alice Smith",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes",
    ),
    "p002": Patient(
        identifier="p002",
        name="Bob Johnson",
        age=45,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Medication B, Diet plan",
    ),
}


def get_patient_by_id(patient_identifier: str) -> Patient:
    """
    Retrieve a patient by identifier.

    Raises:
        ValueError: If the identifier does not exist.
    """
    patient = _PATIENT_DB.get(patient_identifier)
    if patient is None:
        raise ValueError(f"Patient ID '{patient_identifier}' not found.")
    return patient


# --------------------------------------------------------------------------- #
# Report assembly
# --------------------------------------------------------------------------- #

_ALLOWED_PLACEHOLDERS = {"patient.name", "patient.age", "patient.gender"}
_RESTRICTED_PLACEHOLDERS = {"patient.diagnosis", "patient.treatment_plan"}

# Regex to find all `{...}` placeholders
_PLACEHOLDER_RE = re.compile(r"{([^{}]+)}")


def assemble_patient_report(patient_identifier: str, report_template: str) -> str:
    """
    Generate a patient‑specific report from a template.

    Args:
        patient_identifier: The unique identifier of the patient.
        report_template: A string containing placeholders like `{patient.name}`.

    Returns:
        The formatted report as a string.

    Raises:
        ValueError: If the patient ID is invalid or if restricted information
                    is requested in the template.
    """
    # 1. Retrieve patient data
    patient = get_patient_by_id(patient_identifier)

    # 2. Identify placeholders in the template
    placeholders = set(match.group(1) for match in _PLACEHOLDER_RE.finditer(report_template))

    # 3. Validate placeholders
    for ph in placeholders:
        if ph in _RESTRICTED_PLACEHOLDERS:
            raise ValueError(f"Access to restricted field '{ph}' is not allowed.")
        if ph not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Unknown placeholder '{ph}'.")

    # 4. Build a mapping for substitution
    patient_dict = asdict(patient)
    # Map `patient.name` -> patient name, etc.
    mapping: Dict[str, str] = {
        "patient.name": patient_dict["name"],
        "patient.age": str(patient_dict["age"]),
        "patient.gender": patient_dict["gender"],
    }

    # 5. Perform safe formatting
    try:
        formatted_report = report_template.format(**mapping)
    except KeyError as exc:  # pragma: no cover
        raise ValueError(f"Missing data for placeholder {exc}") from exc

    return formatted_report


# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "==============\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(assemble_patient_report("p001", template))