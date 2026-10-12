#!/usr/bin/env python3
"""
Healthcare reporting helper.

This module defines a minimal Patient model and a function to generate
non‑sensitive patient reports from a user supplied template.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict


# --------------------------------------------------------------------------- #
# 1. Patient model and in‑memory store
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    """A simple patient record."""
    uid: str
    name: str
    age: int
    gender: str
    diagnosis: str = field(repr=False)          # Sensitive – hidden in repr
    treatment_plan: str = field(repr=False)     # Sensitive


# In‑memory patient store – in a real system this would be a DB lookup
_PATIENT_STORE: Dict[str, Patient] = {
    "001": Patient(
        uid="001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes and medication"
    ),
    "002": Patient(
        uid="002",
        name="Jane Smith",
        age=32,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler therapy"
    ),
}


# --------------------------------------------------------------------------- #
# 2. Utility: safe placeholder extraction
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}


def _extract_placeholders(template: str) -> set[str]:
    """
    Return a set of placeholder names found in the template.
    Uses a simple regex to find {patient.<field>} patterns.
    """
    pattern = r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}"
    return set(re.findall(pattern, template))


# --------------------------------------------------------------------------- #
# 3. Public API
# --------------------------------------------------------------------------- #

def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Generate a patient report from the supplied schema.

    Parameters
    ----------
    patient_uid : str
        Unique identifier of the patient.
    report_schema : str
        Template string containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted report string containing only non‑sensitive data.

    Raises
    ------
    ValueError
        If the patient is not found or if the template references sensitive
        information (diagnosis or treatment_plan).
    """
    # Retrieve patient record
    patient = _PATIENT_STORE.get(patient_uid)
    if not patient:
        raise ValueError(f"Patient with UID '{patient_uid}' not found.")

    # Check for sensitive placeholders
    placeholders = _extract_placeholders(report_schema)
    if any(field in _SENSITIVE_FIELDS for field in placeholders):
        raise ValueError(
            "Template contains sensitive fields that are not allowed "
            f"({', '.join(_SENSITIVE_FIELDS & placeholders)})"
        )

    # Build mapping for safe formatting
    patient_dict = {
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
    }

    try:
        report = report_schema.format(patient=patient_dict)
    except KeyError as exc:
        # Unrecognized placeholder – treat as error
        raise ValueError(f"Unknown field in template: {exc}") from None

    return report


# --------------------------------------------------------------------------- #
# 4. Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    schema = "Patient {patient.name}, Age: {patient.age}, Gender: {patient.gender}."
    print(compose_patient_report("001", schema))