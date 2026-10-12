#!/usr/bin/env python3
"""
Patient summary generator

This module implements a secure template rendering function that replaces
placeholders such as `{patient.name}` with values from a Patient object.
It validates the patient ID, limits accessible attributes to a safe list,
and protects against accidental exposure of sensitive data.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, fields
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Data model and in‑memory store (for demonstration purposes)
# --------------------------------------------------------------------------- #

@dataclass
class Patient:
    """Represents a patient record."""
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str


# Simulated database of patients (patient_id -> Patient)
PATIENT_DB: Dict[str, Patient] = {
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
        diagnosis="Diabetes Type II",
        treatment_plan="Insulin therapy"
    ),
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_patient(patient_id: str) -> Patient:
    """
    Retrieve a patient by ID. Raises ValueError if not found.
    """
    patient = PATIENT_DB.get(patient_id)
    if patient is None:
        raise ValueError(f"Invalid patient ID: {patient_id}")
    return patient


def _allowed_attributes() -> set[str]:
    """
    Return the set of attribute names that are safe to expose in templates.
    """
    # Exclude any attributes that might be considered sensitive or internal
    return {"name", "age", "gender"}


def _render_template(template: str, context: Dict[str, Any]) -> str:
    """
    Render the template safely by restricting format fields to the provided context.
    Raises ValueError if an unknown field is encountered.
    """
    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"{([^{}]+)}")
    for field_name in placeholder_pattern.findall(template):
        if field_name not in context:
            raise ValueError(f"Unknown template placeholder: {field_name}")
    try:
        return template.format(**context)
    except KeyError as exc:  # pragma: no cover
        raise ValueError(f"Missing value for placeholder {exc}") from exc


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def generate_patient_summary(patient_id: str, report_template: str) -> str:
    """
    Generate a patient summary by filling the provided template with data.

    Args:
        patient_id: The unique identifier of the patient.
        report_template: A string containing placeholders such as
            '{patient.name}', '{patient.age}', etc.

    Returns:
        A string with placeholders replaced by actual patient data.

    Raises:
        ValueError: If the patient ID is invalid or if a restricted attribute
                    is accessed in the template.
    """
    # Retrieve patient data securely
    patient = _get_patient(patient_id)

    # Build context with only allowed attributes
    allowed_attrs = _allowed_attributes()
    patient_dict: Dict[str, Any] = {
        f"patient.{attr}": getattr(patient, attr)
        for attr in allowed_attrs
    }

    # Detect any attempt to access restricted data (e.g., diagnosis)
    # by scanning the template for forbidden patterns
    forbidden_patterns = re.compile(r"{patient\.(diagnosis|treatment_plan)}")
    if forbidden_patterns.search(report_template):
        raise ValueError("Attempt to access restricted medical data in template")

    # Render the template
    return _render_template(report_template, patient_dict)


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = "Patient {patient.name}, Age: {patient.age}, Gender: {patient.gender}."
    print(generate_patient_summary("p001", tmpl))