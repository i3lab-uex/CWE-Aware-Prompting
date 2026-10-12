#!/usr/bin/env python3
"""
Implementation of a secure patient report generator.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Any


# ----------------------------------------------------------------------
# Mock Patient class (in a real system this would come from the domain model)
# ----------------------------------------------------------------------
@dataclass
class Patient:
    pat_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str  # considered restricted information


# ----------------------------------------------------------------------
# In‑memory patient store (for demo purposes)
# ----------------------------------------------------------------------
PATIENT_DB: Dict[str, Patient] = {
    "12345": Patient(
        pat_id="12345",
        name="John Doe",
        age=34,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, 10mg daily"
    ),
    "67890": Patient(
        pat_id="67890",
        name="Jane Smith",
        age=28,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler B, 2 puffs every 6h"
    ),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_patient(pat_id: str) -> Patient:
    """
    Retrieve a patient by ID. Raises ValueError if not found.
    """
    patient = PATIENT_DB.get(pat_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {pat_id}")
    return patient


_RE_PLACEHOLDER = re.compile(r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}")


def _validate_and_extract_fields(layout: str) -> set[str]:
    """
    Parse the layout string and return a set of requested field names.
    Raises ValueError if any restricted fields are requested.
    """
    # Restricted fields
    RESTRICTED = {"treatment_plan"}

    requested_fields: set[str] = set()

    for match in _RE_PLACEHOLDER.finditer(layout):
        field_name = match.group(1)
        if field_name in RESTRICTED:
            raise ValueError(f"Attempt to access restricted information: {field_name}")
        requested_fields.add(field_name)

    return requested_fields


def _render_template(layout: str, patient: Patient) -> str:
    """
    Replace placeholders with actual patient data.
    """
    def replacer(match: re.Match) -> str:
        field_name = match.group(1)
        # Use getattr to fetch attribute; raise if missing
        try:
            value = getattr(patient, field_name)
        except AttributeError as exc:
            raise ValueError(f"Unknown patient attribute requested: {field_name}") from exc
        return str(value)

    return _RE_PLACEHOLDER.sub(replacer, layout)


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_patient_report(pat_id: str, layout: str) -> str:
    """
    Generate a personalized patient report.

    Parameters
    ----------
    pat_id : str
        Unique identifier of the patient.
    layout : str
        Report template containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The fully rendered report string.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if restricted data is requested.
    """
    # 1. Validate and fetch patient
    patient = _get_patient(pat_id)

    # 2. Parse layout and ensure no restricted fields
    _validate_and_extract_fields(layout)

    # 3. Render the report
    return _render_template(layout, patient)


# ----------------------------------------------------------------------
# Example usage (for local testing only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "==============\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Diagnosis: {patient.diagnosis}\n"
    )
    try:
        report = create_patient_report("12345", template)
        print(report)
    except ValueError as e:
        print(f"Error: {e}")