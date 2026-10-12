#!/usr/bin/env python3
"""
Utility to compose patient reports from a template.

The function `compose_patient_report` retrieves a patient record by UID and
substitutes placeholders in the supplied template with non‑sensitive fields.
Attempts to reference sensitive data (diagnosis or treatment_plan) raise
`ValueError`.

The module contains a minimal in‑memory patient store for demonstration.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, ClassVar


# --------------------------------------------------------------------------- #
#  Data model and in‑memory store
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    uid: str
    name: str
    age: int
    gender: str
    diagnosis: str  # sensitive
    treatment_plan: str  # sensitive


class PatientStore:
    """
    Simple in‑memory patient store.
    In a real system this would interface with a database or external API.
    """
    _store: ClassVar[Dict[str, Patient]] = {}

    @classmethod
    def add_patient(cls, patient: Patient) -> None:
        cls._store[patient.uid] = patient

    @classmethod
    def get_patient(cls, uid: str) -> Patient:
        try:
            return cls._store[uid]
        except KeyError as exc:
            raise ValueError(f"Patient with UID '{uid}' not found") from exc


# --------------------------------------------------------------------------- #
#  Report composition
# --------------------------------------------------------------------------- #

# Fields that are allowed to be referenced in the template.
ALLOWED_FIELDS = {"name", "age", "gender"}

# Regex to find all `{field}` placeholders in the template.
PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")


def _validate_template(template: str) -> None:
    """
    Ensure that all placeholders refer to non‑sensitive fields.
    Raises ValueError if a sensitive field is requested or an unknown field
    is used.
    """
    for match in PLACEHOLDER_RE.finditer(template):
        field_name = match.group(1)
        if field_name not in ALLOWED_FIELDS:
            raise ValueError(
                f"Template references disallowed or unknown field '{field_name}'. "
                "Only name, age, and gender are permitted."
            )


def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Generate a patient report by applying the supplied template to the
    patient's non‑sensitive information.

    Parameters
    ----------
    patient_uid : str
        Unique identifier of the patient.
    report_schema : str
        Template string containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient UID is unknown or if the template references a
        sensitive field (diagnosis or treatment_plan) or an unknown field.
    """
    # Fetch patient record
    patient = PatientStore.get_patient(patient_uid)

    # Normalise template: strip optional "patient." prefix
    normalized_template = report_schema.replace("{patient.", "{").replace("patient.}", "}")
    _validate_template(normalized_template)

    # Prepare mapping for str.format
    format_map = {field: getattr(patient, field) for field in ALLOWED_FIELDS}

    try:
        return normalized_template.format(**format_map)
    except KeyError as exc:  # pragma: no cover
        raise ValueError(f"Missing field in template: {exc}") from exc


# --------------------------------------------------------------------------- #
#  Example usage (for testing purposes)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Add a sample patient
    PatientStore.add_patient(
        Patient(
            uid="12345",
            name="John Doe",
            age=38,
            gender="Male",
            diagnosis="Hypertension",
            treatment_plan="Medication A, Lifestyle changes",
        )
    )

    # Valid report
    template = "Patient {patient.name}, age {patient.age}, gender {patient.gender}."
    print(compose_patient_report("12345", template))

    # Attempt to include sensitive data (should raise ValueError)
    try:
        bad_template = "Diagnosis: {patient.diagnosis}"
        compose_patient_report("12345", bad_template)
    except ValueError as e:
        print(f"Error: {e}")