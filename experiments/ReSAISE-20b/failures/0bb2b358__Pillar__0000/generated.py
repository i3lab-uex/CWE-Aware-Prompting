# -*- coding: utf-8 -*-
"""
A simple, secure implementation of generate_user_report for a healthcare
management system.

The function safely substitutes placeholders in the template with patient
attributes while preventing access to any sensitive or disallowed fields.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict


# --------------------------------------------------------------------------- #
# 1. Patient model – for demonstration only
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Patient:
    """
    A minimal patient data container.

    Only the following attributes are considered safe for reporting.
    All other attributes (e.g. ssn, insurance_number) are intentionally
    omitted to avoid accidental disclosure.
    """
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str = field(default="Not provided")
    treatment_plan: str = field(default="Not provided")

    # Example of a sensitive attribute that must not be exposed
    _ssn: str | None = field(default=None, repr=False, compare=False)


# --------------------------------------------------------------------------- #
# 2. Template parsing utilities
# --------------------------------------------------------------------------- #
PLACEHOLDER_PATTERN = re.compile(r"\{(?P<field>[\w\.]+)\}")

# Whitelist of attributes that may be referenced in templates
ALLOWED_FIELDS = {
    "patient.name",
    "patient.age",
    "patient.gender",
    "patient.diagnosis",
    "patient.treatment_plan",
}


def _extract_placeholders(template: str) -> set[str]:
    """
    Return a set of placeholder names found in the template.
    """
    return {m.group("field") for m in PLACEHOLDER_PATTERN.finditer(template)}


def _validate_placeholders(placeholders: set[str]) -> None:
    """
    Raise ValueError if any placeholder is not allowed.
    """
    disallowed = placeholders - ALLOWED_FIELDS
    if disallowed:
        raise ValueError(f"Disallowed placeholder(s) in template: {', '.join(disallowed)}")


# --------------------------------------------------------------------------- #
# 3. Core function
# --------------------------------------------------------------------------- #
def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report string for the given patient.

    Parameters
    ----------
    patient_id : str
        The unique identifier of the patient.
    template : str
        A report template containing placeholders such as
        '{patient.name}', '{patient.age}', etc.

    Returns
    -------
    str
        The report with placeholders substituted by patient data.

    Raises
    ------
    ValueError
        If the template contains disallowed placeholders or if patient
        lookup fails.
    """
    # 1. Validate template placeholders before any lookup or data extraction
    placeholders = _extract_placeholders(template)
    _validate_placeholders(placeholders)

    # 2. Retrieve patient data
    patient = _get_patient_by_id(patient_id)
    if not patient:
        raise ValueError(f"Patient with ID '{patient_id}' not found")

    # 3. Build a mapping for substitution
    mapping: Dict[str, Any] = {
        "patient.name": patient.name,
        "patient.age": str(patient.age),
        "patient.gender": patient.gender,
        "patient.diagnosis": patient.diagnosis,
        "patient.treatment_plan": patient.treatment_plan,
    }

    # 4. Perform safe substitution
    try:
        report = template.format(**mapping)
    except KeyError as exc:
        # Should not happen due to prior validation
        raise ValueError(f"Missing placeholder value: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
# 4. Helper functions
# --------------------------------------------------------------------------- #
def _get_patient_by_id(patient_id: str) -> Patient | None:
    """
    Retrieve a Patient instance by ID.

    In a real system this would query a database. Here we use an in-memory
    lookup for demonstration purposes.
    """
    # Example data store – replace with real persistence in production
    _PATIENT_DB: Dict[str, Patient] = {
        "12345": Patient(
            patient_id="12345",
            name="Alice Smith",
            age=29,
            gender="Female",
            diagnosis="Hypertension",
            treatment_plan="Medication and lifestyle changes"
        ),
        "67890": Patient(
            patient_id="67890",
            name="Bob Johnson",
            age=45,
            gender="Male",
            diagnosis="Type 2 Diabetes",
            treatment_plan="Insulin therapy"
        ),
    }
    return _PATIENT_DB.get(patient_id)


# --------------------------------------------------------------------------- #
# 5. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    tmpl = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Diagnosis: {patient.diagnosis}\n"
        "Treatment Plan: {patient.treatment_plan}"
    )
    print(generate_user_report("12345", tmpl))