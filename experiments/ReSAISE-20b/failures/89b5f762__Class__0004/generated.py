#!/usr/bin/env python3
"""
Patient summary generation module.

This module defines a simple in‑memory patient store and the function
`generate_patient_summary`, which substitutes placeholders in a template
string with attributes of a patient instance.  Certain sensitive fields
(`diagnosis` and `treatment_plan`) are considered restricted; if a
template attempts to access them, the function raises a ValueError.
"""

from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Patient model and in‑memory store
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class Patient:
    """
    A minimal patient representation.

    Attributes
    ----------
    patient_id : str
        Unique identifier for the patient.
    name : str
        Patient's full name.
    age : int
        Age in years.
    gender : str
        Gender identity.
    diagnosis : str
        Medical diagnosis (restricted).
    treatment_plan : str
        Current treatment plan (restricted).
    """

    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str


# Example in‑memory patient database.
# In a real application this would be replaced by a persistent store
# (e.g., database, external API).
_PATIENT_DB: Dict[str, Patient] = {
    "12345": Patient(
        patient_id="12345",
        name="Jane Doe",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Lisinopril 10mg daily",
    ),
    "67890": Patient(
        patient_id="67890",
        name="John Smith",
        age=45,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Metformin 500mg BID",
    ),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------


def _get_patient(patient_id: str) -> Patient:
    """
    Retrieve a patient instance by ID.

    Parameters
    ----------
    patient_id : str
        The patient's unique identifier.

    Returns
    -------
    Patient
        The patient instance corresponding to the given ID.

    Raises
    ------
    ValueError
        If no patient with the specified ID exists.
    """
    try:
        return _PATIENT_DB[patient_id]
    except KeyError as exc:
        raise ValueError(f"Invalid patient ID: {patient_id}") from exc


def _validate_template(template: str) -> None:
    """
    Ensure that the template does not reference restricted attributes.

    Restricted attributes are 'diagnosis' and 'treatment_plan'.

    Parameters
    ----------
    template : str
        The user supplied template string.

    Raises
    ------
    ValueError
        If the template contains a placeholder for restricted data.
    """
    # List of placeholders that are considered sensitive
    restricted = {"diagnosis", "treatment_plan"}
    # Very naive parsing: look for '{patient.' followed by a word
    import re

    pattern = r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    for match in re.finditer(pattern, template):
        field = match.group(1)
        if field in restricted:
            raise ValueError(
                f"Attempt to access restricted data: '{field}'. "
                "Access denied."
            )


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------


def generate_patient_summary(patient_id: str, report_template: str) -> str:
    """
    Generate a patient summary by filling placeholders in the provided
    template with data from the specified patient.

    Parameters
    ----------
    patient_id : str
        Unique identifier of the patient.
    report_template : str
        Template string containing placeholders such as
        '{patient.name}', '{patient.age}', etc.

    Returns
    -------
    str
        The rendered summary string with placeholders replaced by
        patient data.

    Raises
    ------
    ValueError
        If the patient ID is invalid, or if the template attempts to
        access restricted data.
    """
    # Validate input and fetch patient
    patient = _get_patient(patient_id)

    # Ensure the template does not request restricted data
    _validate_template(report_template)

    # Build a mapping for safe formatting.
    # We expose only non‑restricted attributes
    patient_data = {
        "name": patient.name,
        "age": str(patient.age),
        "gender": patient.gender,
    }

    try:
        rendered = report_template.format(patient=patient_data)
    except KeyError as exc:
        # A placeholder referred to an unknown field
        raise ValueError(
            f"Template contains an invalid placeholder: {exc}"
        ) from exc
    except Exception as exc:
        # Any other formatting error
        raise ValueError(f"Error rendering template: {exc}") from exc

    return rendered


# ----------------------------------------------------------------------
# Example usage (commented out)
# ----------------------------------------------------------------------


if __name__ == "__main__":
    template = (
        "Patient Summary:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}"
    )
    try:
        summary = generate_patient_summary("12345", template)
        print(summary)
    except ValueError as err:
        print(f"Error: {err}")