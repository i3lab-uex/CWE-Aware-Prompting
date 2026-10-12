#!/usr/bin/env python3
"""
Utility for generating patient summaries from a template string.
The module is intentionally lightweight and avoids any external
dependencies beyond the Python standard library.

Author:  <your name>
Date:    2026-07-23
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------------------------------------------------------- #
# Data model & in‑memory store
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    """
    Represents a patient record.

    Attributes
    ----------
    patient_id : str
        Unique identifier for the patient.
    name       : str
        Patient's full name.
    age        : int
        Patient's age in years.
    gender     : str
        Patient's gender (e.g., 'Male', 'Female', 'Other').
    diagnosis  : str
        Current diagnosis (restricted data).
    treatment_plan : str
        Treatment plan details (restricted data).
    """
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str


# In‑memory patient store (in a real system this would be a database).
PATIENT_STORE: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Prescribed 10mg Lisinopril daily.",
    ),
    "P002": Patient(
        patient_id="P002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Metformin 500mg BID and diet modification.",
    ),
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

# Allowed placeholders for the public report.
ALLOWED_FIELDS = {"name", "age", "gender"}

# Regex pattern to find placeholders in the form {patient.<field>}
PLACEHOLDER_PATTERN = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _extract_placeholders(template: str) -> set[str]:
    """Return a set of field names found in the template."""
    return {match.group(1) for match in PLACEHOLDER_PATTERN.finditer(template)}

def _get_patient_by_id(patient_id: str) -> Patient:
    """Retrieve a patient object by ID or raise ValueError."""
    try:
        return PATIENT_STORE[patient_id]
    except KeyError as exc:
        raise ValueError(f"Patient ID '{patient_id}' not found.") from exc


# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def generate_patient_summary(patient_id: str, report_template: str) -> str:
    """
    Generate a patient summary by filling placeholders in the template.

    Parameters
    ----------
    patient_id : str
        Unique identifier of the patient.
    report_template : str
        Template string containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if the template attempts to access
        restricted data (diagnosis, treatment_plan, etc.).
    """
    # 1. Validate patient ID and fetch record
    patient = _get_patient_by_id(patient_id)

    # 2. Detect placeholders in the template
    placeholders = _extract_placeholders(report_template)

    # 3. Ensure no restricted fields are requested
    if not placeholders <= ALLOWED_FIELDS:
        # Compute the intersection of disallowed fields for a clearer error
        disallowed = placeholders - ALLOWED_FIELDS
        raise ValueError(
            f"Template contains restricted fields: {', '.join(sorted(disallowed))}"
        )

    # 4. Build a mapping of field names to values
    patient_dict = asdict(patient)
    # Only expose allowed fields
    context = {field: patient_dict[field] for field in placeholders}

    # 5. Perform safe formatting
    try:
        result = report_template.format(patient=context)
    except KeyError as exc:  # pragma: no cover
        # This should not happen due to earlier checks, but guard anyway.
        raise ValueError(f"Missing placeholder data for field '{exc.args[0]}'") from exc

    return result


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Patient Summary:\n"
        "- Name: {patient.name}\n"
        "- Age: {patient.age} years\n"
        "- Gender: {patient.gender}\n"
    )
    try:
        print(generate_patient_summary("P001", template))
    except ValueError as err:
        print(f"Error: {err}")