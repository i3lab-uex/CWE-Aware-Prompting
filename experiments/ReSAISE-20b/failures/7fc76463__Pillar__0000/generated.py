# -*- coding: utf-8 -*-
"""
Patient summary report builder.

This module provides a single public function, :func:`build_patient_summary`,
which replaces placeholders in a report template with values taken from a
``Patient`` instance identified by ``identifier``.

The function protects against:
* Invalid patient identifiers.
* Unauthorized access to sensitive fields (``diagnosis`` and ``treatment_plan``).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# 1. Domain model – Patient
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    """Represents a patient record in the system."""
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str = field(repr=False)
    treatment_plan: str = field(repr=False)

    # A simple lookup table emulating a database
    _PATIENT_DB: Dict[str, "Patient"] = field(default_factory=dict, init=False, repr=False)

    @classmethod
    def register(cls, patient: "Patient") -> None:
        """Adds a patient to the internal database."""
        cls._PATIENT_DB[patient.id] = patient

    @classmethod
    def get(cls, identifier: str) -> "Patient":
        """Retrieves a patient by ID or raises KeyError."""
        return cls._PATIENT_DB[identifier]


# --------------------------------------------------------------------------- #
# 2. Report builder
# --------------------------------------------------------------------------- #

PLACEHOLDER_PATTERN = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

# Fields that are considered sensitive and cannot be exposed in the report
RESTRICTED_FIELDS = {"diagnosis", "treatment_plan"}


def _resolve_placeholder(match: re.Match, patient: Patient) -> str:
    """Return the string value for a single placeholder."""
    field_name = match.group(1)

    if field_name in RESTRICTED_FIELDS:
        raise ValueError(f"Access to restricted patient data: '{field_name}'")

    try:
        value = getattr(patient, field_name)
    except AttributeError as exc:
        raise ValueError(f"Unknown placeholder: 'patient.{field_name}'") from exc

    # Convert non-string values to string
    return str(value)


def build_patient_summary(identifier: str, report_template: str) -> str:
    """
    Build a personalized patient summary from ``report_template``.

    Parameters
    ----------
    identifier : str
        Unique identifier for the patient.
    report_template : str
        Text containing placeholders such as ``{patient.name}``.

    Returns
    -------
    str
        The report with placeholders replaced by patient data.

    Raises
    ------
    ValueError
        If the identifier is unknown, or if a placeholder refers to a restricted
        field or an invalid attribute.
    """
    # 1. Retrieve the patient record – this may raise KeyError
    try:
        patient = Patient.get(identifier)
    except KeyError as exc:
        raise ValueError(f"Invalid patient identifier: '{identifier}'") from exc

    # 2. Replace placeholders safely
    try:
        result = PLACEHOLDER_PATTERN.sub(
            lambda m: _resolve_placeholder(m, patient), report_template
        )
    except ValueError as exc:
        # Re‑raise so the caller can handle it
        raise

    return result


# --------------------------------------------------------------------------- #
# 3. Example usage (commented out – for illustration only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Register a patient (in a real system this would be persistent storage)
    Patient.register(
        Patient(
            id="12345",
            name="Jane Doe",
            age=29,
            gender="Female",
            diagnosis="Hypertension",
            treatment_plan="Medication A, 5mg daily",
        )
    )

    template = (
        "Patient Report\n"
        "==============\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )

    print(build_patient_summary("12345", template))