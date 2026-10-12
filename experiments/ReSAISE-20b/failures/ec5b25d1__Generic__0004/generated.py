#!/usr/bin/env python3
"""
Healthcare reporting helper.

Provides a function `create_person_report` that renders a report string for a patient,
substituting placeholders such as `{patient.name}` with the actual data.
Access to sensitive fields (diagnosis, treatment_plan) is prohibited and will raise
`ValueError`.

The module includes a minimal in‑memory patient store for demonstration purposes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, ClassVar


# --------------------------------------------------------------------------- #
#  Patient model & in‑memory store
# --------------------------------------------------------------------------- #

@dataclass
class Patient:
    """Represents a patient record."""
    code: str  # unique identifier
    name: str
    age: int
    gender: str
    diagnosis: str  # sensitive
    treatment_plan: str  # sensitive

    # A simple in‑memory registry of patients.
    _registry: ClassVar[Dict[str, "Patient"]] = {}

    def __post_init__(self) -> None:
        """Register the patient in the global store."""
        if self.code in Patient._registry:
            raise ValueError(f"Duplicate patient code: {self.code}")
        Patient._registry[self.code] = self

    @classmethod
    def get_by_code(cls, code: str) -> "Patient":
        """Retrieve a patient by code or raise ValueError."""
        try:
            return cls._registry[code]
        except KeyError as exc:
            raise ValueError(f"Patient with code '{code}' not found") from exc


# --------------------------------------------------------------------------- #
#  Report generation
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
_PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")


def create_person_report(patient_code: str, report_template: str) -> str:
    """
    Render a report for the patient identified by *patient_code* using
    *report_template*.

    The template may contain placeholders of the form `{patient.field}`.
    Only non‑sensitive fields are allowed; attempting to use a sensitive
    field results in a :class:`ValueError`.

    Parameters
    ----------
    patient_code:
        The unique identifier for the patient.
    report_template:
        A string containing placeholders to be replaced.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient cannot be found or if a sensitive field is referenced.
    """
    # Retrieve patient
    patient = Patient.get_by_code(patient_code)

    # Find all placeholders in the template
    placeholders = _PLACEHOLDER_RE.findall(report_template)

    # Ensure no sensitive fields are used
    for field_name in placeholders:
        if field_name in _SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{field_name}' is forbidden")

    # Build a mapping of allowed fields
    allowed_data = {
        name: getattr(patient, name)
        for name in placeholders
        if hasattr(patient, name)
    }

    # Verify that all placeholders have corresponding data
    missing = set(placeholders) - allowed_data.keys()
    if missing:
        raise ValueError(f"Missing patient attributes: {', '.join(missing)}")

    # Perform formatting
    try:
        return report_template.format(**{"patient": allowed_data})
    except KeyError as exc:
        raise ValueError(f"Missing placeholder data: {exc}") from exc


# --------------------------------------------------------------------------- #
#  Demo / Test
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create a sample patient
    Patient(
        code="P001",
        name="Alice Smith",
        age=34,
        gender="F",
        diagnosis="Hypertension",
        treatment_plan="Medication and lifestyle changes",
    )

    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age} years\n"
        "Gender: {patient.gender}\n"
    )

    print(create_person_report("P001", template))

    # The following will raise ValueError because of a sensitive field
    try:
        bad_template = "Diagnosis: {patient.diagnosis}"
        print(create_person_report("P001", bad_template))
    except ValueError as e:
        print(f"Error: {e}")