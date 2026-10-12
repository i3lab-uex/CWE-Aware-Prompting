#!/usr/bin/env python3
"""
Patient summary builder

This module defines a simple in‑memory patient store and the
`build_patient_summary` function which applies a user supplied
template to a patient's non‑sensitive data.  Any attempt to expose
diagnostic or treatment information is rejected with a ValueError.
"""

from __future__ import annotations

import string
from dataclasses import dataclass, field
from typing import Dict


# --------------------------------------------------------------------------- #
# 1. Patient model & in‑memory store
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    """Simple patient record."""
    key: str
    name: str
    age: int
    gender: str
    # Sensitive fields – not to be exposed through the public API
    diagnosis: str = field(repr=False)
    treatment_plan: str = field(repr=False)


# In‑memory registry of patients
PATIENT_REGISTRY: Dict[str, Patient] = {
    "P001": Patient(
        key="P001",
        name="Alice Smith",
        age=29,
        gender="F",
        diagnosis="Hypertension",
        treatment_plan="Medication A, lifestyle changes",
    ),
    "P002": Patient(
        key="P002",
        name="Bob Jones",
        age=45,
        gender="M",
        diagnosis="Diabetes Type 2",
        treatment_plan="Insulin therapy, diet modification",
    ),
}


# --------------------------------------------------------------------------- #
# 2. Helper functions
# --------------------------------------------------------------------------- #

def _get_patient(patient_key: str) -> Patient:
    """
    Retrieve a patient from the registry.

    Raises ValueError if the key is not present.
    """
    try:
        return PATIENT_REGISTRY[patient_key]
    except KeyError as exc:
        raise ValueError(f"Patient with key '{patient_key}' not found") from exc


def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference sensitive fields.

    Raises ValueError if a disallowed field is detected.
    """
    # Disallowed placeholders
    disallowed = {"diagnosis", "treatment_plan"}
    formatter = string.Formatter()
    for _, field_name, _, _ in formatter.parse(template):
        if field_name is None:
            continue
        # Handle nested attributes like patient.name -> split by '.'
        parts = field_name.split(".")
        if parts[0] == "patient" and len(parts) > 1:
            attr = parts[1]
            if attr in disallowed:
                raise ValueError(
                    f"Template attempts to expose sensitive information: '{field_name}'"
                )
        else:
            # Any other top‑level field is disallowed
            raise ValueError(
                f"Template contains unsupported placeholder: '{field_name}'"
            )


# --------------------------------------------------------------------------- #
# 3. Public API
# --------------------------------------------------------------------------- #

def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Generate a patient summary string from the supplied template.

    Parameters
    ----------
    patient_key : str
        Identification code of the patient.
    template_string : str
        Template containing placeholders like '{patient.name}' or '{patient.age}'.

    Returns
    -------
    str
        The rendered summary string.

    Raises
    ------
    ValueError
        If the patient is not found or if the template references sensitive data.
    """
    # Retrieve patient record
    patient = _get_patient(patient_key)

    # Validate template safety
    _validate_template(template_string)

    # Prepare mapping for formatting
    mapping = {"patient": patient}

    try:
        return template_string.format(**mapping)
    except KeyError as exc:
        # This should not happen because we validated the template
        raise ValueError(f"Missing data for placeholder: {exc}") from exc


# --------------------------------------------------------------------------- #
# 4. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = "Patient {patient.name}, age {patient.age}, gender {patient.gender}."
    print(build_patient_summary("P001", tmpl))

    # This will raise ValueError due to sensitive field
    # bad_tmpl = "Diagnosis: {patient.diagnosis}"
    # print(build_patient_summary("P001", bad_tmpl))