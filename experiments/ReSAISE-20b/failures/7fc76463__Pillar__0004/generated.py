# -*- coding: utf-8 -*-
"""
Utility to generate a patient summary report from a template.

The function `build_patient_summary` performs the following steps:

1. Validates that the patient ID exists in the data store.
2. Checks the template for any disallowed placeholders (e.g. accessing
   sensitive fields such as `diagnosis`).
3. Replaces all placeholders of the form `{patient.<field>}` with the
   corresponding attribute value from the `Patient` instance.
4. Returns the fully rendered report.

The implementation avoids leaking any resources (e.g. file handles) and
uses a regular expression to safely perform placeholder substitution,
thereby mitigating CWE‑664 (Improper Control of a Resource Through its
Lifetime) and preventing accidental exposure of restricted data.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict


# --------------------------------------------------------------------------- #
#  Data model & in‑memory data store                                           #
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    """Simple patient data model."""
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str  # Sensitive information
    treatment_plan: str

# Simulated patient database (in‑memory). In a real system this would be
# replaced by a proper persistence layer.
_PATIENT_DB: Dict[str, Patient] = {
    "p001": Patient(
        id="p001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "p002": Patient(
        id="p002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Diabetes Type 2",
        treatment_plan="Insulin therapy, Diet plan"
    ),
}


# --------------------------------------------------------------------------- #
#  Helper functions                                                            #
# --------------------------------------------------------------------------- #

def _get_patient(patient_id: str) -> Patient:
    """
    Retrieve a patient from the data store.
    Raises ValueError if the ID does not exist.
    """
    try:
        return _PATIENT_DB[patient_id]
    except KeyError as exc:
        raise ValueError(f"Invalid patient ID: {patient_id}") from exc


# --------------------------------------------------------------------------- #
#  Main function                                                               #
# --------------------------------------------------------------------------- #

def build_patient_summary(identifier: str, report_template: str) -> str:
    """
    Generate a patient summary by replacing placeholders in the template.

    Parameters
    ----------
    identifier : str
        Unique patient identifier.
    report_template : str
        Report template containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The fully rendered report.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if a restricted field is requested.
    """
    # 1. Retrieve the patient record
    patient = _get_patient(identifier)

    # 2. Define allowed (non‑restricted) fields
    #    In this example we treat `diagnosis` as restricted.
    allowed_fields = {
        "name",
        "age",
        "gender",
        "treatment_plan",
    }

    # 3. Prepare a mapping for placeholder substitution
    patient_dict = {
        field: getattr(patient, field) for field in allowed_fields
    }

    # 4. Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = placeholder_pattern.findall(report_template)

    # 5. Validate and replace each placeholder
    rendered_parts = []
    last_end = 0
    for match in placeholder_pattern.finditer(report_template):
        start, end = match.span()
        field_name = match.group(1)

        # Append the literal text before this placeholder
        rendered_parts.append(report_template[last_end:start])

        if field_name not in patient_dict:
            # Either a restricted or unknown field
            if field_name == "diagnosis":
                raise ValueError(
                    f"Access to restricted medical information '{field_name}' is prohibited."
                )
            raise ValueError(f"Unknown placeholder '{{patient.{field_name}}}'.")
        rendered_parts.append(str(patient_dict[field_name]))
        last_end = end

    # Append any remaining literal text after the last placeholder
    rendered_parts.append(report_template[last_end:])

    # 6. Join and return the final report
    return "".join(rendered_parts)


# --------------------------------------------------------------------------- #
#  Example usage (comment out in production)                                 #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "==============\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Treatment Plan: {patient.treatment_plan}\n"
    )
    print(build_patient_summary("p001", template))