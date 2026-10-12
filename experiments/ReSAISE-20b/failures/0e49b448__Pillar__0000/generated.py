#!/usr/bin/env python3
"""
Healthcare reporting system – patient summary builder.
"""

from __future__ import annotations

import dataclasses
import string
from typing import Dict


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclasses.dataclass(frozen=True)
class Patient:
    """
    Immutable patient record.  Only non‑sensitive fields are exposed by the
    reporting system.
    """
    name: str
    age: int
    gender: str

    # Sensitive fields – intentionally omitted from public interface
    _diagnosis: str | None = dataclasses.field(repr=False, default=None)
    _treatment_plan: str | None = dataclasses.field(repr=False, default=None)

    @property
    def diagnosis(self) -> str | None:
        """Internal accessor – not exposed to the report builder."""
        return self._diagnosis

    @property
    def treatment_plan(self) -> str | None:
        """Internal accessor – not exposed to the report builder."""
        return self._treatment_plan


# --------------------------------------------------------------------------- #
# In‑memory patient repository (stand‑in for a database)
# --------------------------------------------------------------------------- #

_patient_store: Dict[str, Patient] = {
    "P001": Patient(
        name="Alice Smith",
        age=29,
        gender="F",
        _diagnosis="Hypertension",
        _treatment_plan="Medication A, Lifestyle changes",
    ),
    "P002": Patient(
        name="Bob Johnson",
        age=45,
        gender="M",
        _diagnosis="Diabetes Type II",
        _treatment_plan="Insulin therapy, Diet plan",
    ),
}


# --------------------------------------------------------------------------- #
# Report builder
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"patient.diagnosis", "patient.treatment_plan"}


def _extract_placeholders(template: str) -> set[str]:
    """
    Parse a format string and return the set of field names used.

    :param template: The format string containing placeholders.
    :return: Set of placeholder names, e.g. {"patient.name", "patient.age"}.
    """
    formatter = string.Formatter()
    return {field_name for _, field_name, _, _ in formatter.parse(template) if field_name}


def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Generate a patient summary string by applying *template_string* to the
    non‑sensitive data of the patient identified by *patient_key*.

    Parameters
    ----------
    patient_key : str
        Identifier for the patient.
    template_string : str
        Format string containing placeholders such as ``{patient.name}``.

    Returns
    -------
    str
        The formatted patient summary.

    Raises
    ------
    ValueError
        If the patient key is unknown, or if the template attempts to access
        sensitive fields (diagnosis or treatment_plan).
    """
    # ----------------------------------------------------------------------- #
    # 1. Retrieve the patient record
    # ----------------------------------------------------------------------- #
    try:
        patient = _patient_store[patient_key]
    except KeyError as exc:
        raise ValueError(f"Patient ID '{patient_key}' not found.") from exc

    # ----------------------------------------------------------------------- #
    # 2. Ensure the template does not request sensitive data
    # ----------------------------------------------------------------------- #
    placeholders = _extract_placeholders(template_string)
    if any(field in _SENSITIVE_FIELDS for field in placeholders):
        raise ValueError("Template contains references to sensitive patient data.")

    # ----------------------------------------------------------------------- #
    # 3. Build a safe mapping for the format operation
    # ----------------------------------------------------------------------- #
    # The mapping keys mimic the placeholders used in the template.
    mapping = {
        "patient.name": patient.name,
        "patient.age": patient.age,
        "patient.gender": patient.gender,
    }

    # ----------------------------------------------------------------------- #
    # 4. Perform formatting
    # ----------------------------------------------------------------------- #
    try:
        result = template_string.format(**mapping)
    except KeyError as exc:
        # This can happen if the template contains a placeholder that is not
        # supported by our mapping (e.g., an unexpected field).
        raise ValueError(f"Unsupported placeholder in template: {exc}") from exc

    return result


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = "Patient {patient.name}, Age: {patient.age}, Gender: {patient.gender}."
    print(build_patient_summary("P001", tmpl))