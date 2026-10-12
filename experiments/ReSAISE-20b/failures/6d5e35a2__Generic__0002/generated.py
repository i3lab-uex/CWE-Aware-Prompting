# -*- coding: utf-8 -*-

"""
Patient reporting module.

This module provides a single public function `create_patient_report` that
generates a personalized report for a patient by substituting placeholders in
a template string with the patient's attributes.

The function performs minimal security checks:
  * The patient ID must exist in the system.
  * Access to "restricted" attributes (those starting with an underscore
    or named `ssn`) is prohibited and will raise a ValueError.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict


# --------------------------------------------------------------------------- #
#  Dummy patient database and Patient model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    """Simple representation of a patient record."""
    pat_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str
    ssn: str | None = field(default=None, repr=False)  # sensitive

# In a real system this would be replaced by a database query
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        pat_id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes",
        ssn="123-45-6789",
    ),
    "P002": Patient(
        pat_id="P002",
        name="Jane Smith",
        age=32,
        gender="Female",
        diagnosis="Diabetes Type 2",
        treatment_plan="Insulin therapy, Diet plan",
    ),
}


# --------------------------------------------------------------------------- #
#  Reporting function
# --------------------------------------------------------------------------- #

PLACEHOLDER_PATTERN = re.compile(r"\{(?P<field>[^}]+)\}")


def _get_patient(pat_id: str) -> Patient:
    """
    Retrieve a patient from the database.

    Raises ValueError if the patient ID is not found.
    """
    try:
        return PATIENT_DB[pat_id]
    except KeyError as exc:
        raise ValueError(f"Invalid patient ID: {pat_id}") from exc


def _is_restricted(field_name: str) -> bool:
    """
    Determine whether a field is considered restricted.

    For this example, any attribute that starts with an underscore or
    is named 'ssn' is considered restricted.
    """
    return field_name.startswith("_") or field_name.lower() == "ssn"


def _replace_placeholder(match: re.Match, patient: Patient) -> str:
    """
    Callback used by `re.sub` to replace a placeholder with the actual value.

    Raises ValueError if attempting to access restricted data or
    if the field does not exist on Patient.
    """
    field_name = match.group("field")

    if _is_restricted(field_name):
        raise ValueError(f"Access to restricted field '{field_name}' is not allowed")

    # Use getattr to fetch the attribute; raise if missing
    try:
        value = getattr(patient, field_name)
    except AttributeError as exc:
        raise ValueError(f"Patient has no attribute '{field_name}'") from exc

    # Convert non-string values to string for formatting
    return str(value)


def create_patient_report(pat_id: str, layout: str) -> str:
    """
    Generate a personalized patient report.

    Parameters
    ----------
    pat_id : str
        The unique identifier of the patient.
    layout : str
        A string containing placeholders in the form `{patient.field}`.

    Returns
    -------
    str
        The formatted report with placeholders substituted by patient data.

    Raises
    ------
    ValueError
        If the patient ID is invalid, if a placeholder refers to restricted data,
        or if a placeholder references an unknown attribute.
    """
    # Retrieve the patient
    patient = _get_patient(pat_id)

    # Find all placeholders that start with 'patient.'
    def placeholder_replacer(match: re.Match) -> str:
        # The full placeholder is something like {patient.name}
        content = match.group("field")
        if not content.startswith("patient."):
            # Preserve the placeholder unchanged
            return match.group(0)

        # Strip the 'patient.' prefix to get the attribute name
        attr_name = content[len("patient.") :]
        return _replace_placeholder(
            re.match(rf"{{{re.escape(attr_name)}}}", f"{{{attr_name}}}"), patient
        )

    # Replace placeholders in the layout
    report = PLACEHOLDER_PATTERN.sub(placeholder_replacer, layout)

    return report


# --------------------------------------------------------------------------- #
#  Example usage (for testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    example_layout = (
        "Patient Report\n"
        "==============\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Diagnosis: {patient.diagnosis}\n"
        "Treatment Plan: {patient.treatment_plan}\n"
    )

    try:
        print(create_patient_report("P001", example_layout))
    except ValueError as e:
        print(f"Error: {e}")