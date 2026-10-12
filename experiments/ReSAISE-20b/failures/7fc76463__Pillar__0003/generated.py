#!/usr/bin/env python3
"""
A minimal implementation of a patient report generator.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Mock data store – in a real system this would be replaced by a database
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Patient:
    """Represents patient information."""
    name: str
    age: int
    gender: str
    diagnosis: str          # Highly sensitive – access is restricted
    treatment_plan: str


# Example patient records
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication: Lisinopril 10mg daily"
    ),
    "P002": Patient(
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler: Albuterol 2 puffs as needed"
    ),
}


# --------------------------------------------------------------------------- #
# Resource handling – ensures that patient data is released correctly
# --------------------------------------------------------------------------- #
class PatientResource:
    """Context manager for safely accessing patient data."""

    def __init__(self, identifier: str):
        self.identifier = identifier
        self.patient: Patient | None = None

    def __enter__(self) -> Patient:
        # Simulate resource acquisition
        self.patient = PATIENT_DB.get(self.identifier)
        if not self.patient:
            raise ValueError(f"Invalid patient ID: {self.identifier}")
        return self.patient

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # Simulate resource release
        self.patient = None


# --------------------------------------------------------------------------- #
# Core functionality – build_patient_summary
# --------------------------------------------------------------------------- #
PLACEHOLDER_PATTERN = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

# Fields that are allowed to be exposed in the report
ALLOWED_FIELDS = {"name", "age", "gender", "treatment_plan"}

# Fields that are restricted (e.g., diagnosis)
RESTRICTED_FIELDS = {"diagnosis"}


def build_patient_summary(identifier: str, report_template: str) -> str:
    """
    Build a personalized patient summary by substituting placeholders
    in the report_template with data from the specified patient.

    Args:
        identifier: The unique patient ID.
        report_template: A string containing placeholders of the form
                         {patient.<field>}.

    Returns:
        The formatted report string.

    Raises:
        ValueError: If the patient ID is invalid, a restricted field
                    is requested, or an unknown placeholder appears.
    """
    # Validate template for restricted fields early
    for match in PLACEHOLDER_PATTERN.finditer(report_template):
        field = match.group(1)
        if field in RESTRICTED_FIELDS:
            raise ValueError(f"Attempt to access restricted field: {field}")

    # Acquire patient data safely
    with PatientResource(identifier) as patient:
        # Build a dictionary of allowed attributes
        data: Dict[str, Any] = {
            key: getattr(patient, key)
            for key in ALLOWED_FIELDS
        }

        # Perform substitution
        def replace(match: re.Match) -> str:
            field = match.group(1)
            if field not in data:
                raise ValueError(f"Unknown placeholder: {field}")
            return str(data[field])

        formatted_report = PLACEHOLDER_PATTERN.sub(replace, report_template)
    return formatted_report


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Treatment Plan: {patient.treatment_plan}\n"
    )
    print(build_patient_summary("P001", template))