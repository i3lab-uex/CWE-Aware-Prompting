#!/usr/bin/env python3
"""
Healthcare reporting module.

This module implements a single public function,
`generate_user_report`, which renders a report for a patient
given a template string.  The template may contain placeholders of
the form `{patient.<attribute>}` which are replaced with the
corresponding attribute values from a :class:`Patient` instance.

The implementation follows best practices for security and
resource handling:
  * Only attributes explicitly listed in ``_ALLOWED_FIELDS`` are
    exposed. This prevents accidental leakage of sensitive data.
  * No external resources (files, network connections, etc.) are
    opened; the function operates purely in memory.
  * Regular expressions are used for placeholder extraction,
    avoiding the use of ``eval`` or other unsafe dynamic code
    execution.
  * Errors are reported via :class:`ValueError` as required.

CWE-664 (Improper Control of a Resource Through its Lifetime) is
avoided because the function does not create or manage any external
resource beyond simple in‑memory objects, and all resources are
automatically released when the function returns.
"""

import re
from dataclasses import dataclass, fields
from typing import Dict

# --------------------------------------------------------------------------- #
# Patient model (simplified for this example)
# --------------------------------------------------------------------------- #

@dataclass
class Patient:
    """
    Represents a patient record.

    Attributes that are considered safe for reporting can be added to
    ``_ALLOWED_FIELDS``.  Attributes not in that list will raise an
    exception if accessed via the template.
    """
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str
    # ... other fields ...

# --------------------------------------------------------------------------- #
# In‑memory "database" lookup (replace with real persistence layer)
# --------------------------------------------------------------------------- #

def _get_patient_by_id(patient_id: str) -> Patient:
    """
    Retrieve a :class:`Patient` instance by its ID.

    For demonstration purposes this function returns a hard‑coded
    patient.  In production, replace this with a database query.
    """
    # Dummy data – in real code fetch from DB, raise if not found
    return Patient(
        patient_id=patient_id,
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication and lifestyle changes"
    )

# --------------------------------------------------------------------------- #
# Report generation
# --------------------------------------------------------------------------- #

# Only expose these fields in the template to avoid leaking sensitive data.
_ALLOWED_FIELDS = {
    "name",
    "age",
    "gender",
    "diagnosis",
    "treatment_plan",
}

_PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _render_template(template: str, context: Dict[str, str]) -> str:
    """
    Replace placeholders in ``template`` using values from ``context``.

    Raises ValueError if a placeholder refers to an unknown key.
    """
    def _replace(match: re.Match) -> str:
        key = match.group(1)
        if key not in context:
            raise ValueError(f"Unknown placeholder: {{patient.{key}}}")
        return str(context[key])

    return _PLACEHOLDER_RE.sub(_replace, template)

def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report string for the patient identified by ``patient_id``.

    Parameters
    ----------
    patient_id : str
        The unique identifier of the patient.
    template : str
        Report template containing placeholders such as ``{patient.name}``.

    Returns
    -------
    str
        The rendered report.

    Raises
    ------
    ValueError
        If the patient cannot be found, if a placeholder refers to an
        unknown or disallowed field, or if any other error occurs during
        rendering.
    """
    # Fetch patient record – in real code handle missing patient
    try:
        patient = _get_patient_by_id(patient_id)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to retrieve patient {patient_id}") from exc

    # Build context dictionary with only allowed fields
    context = {}
    for field_name in _ALLOWED_FIELDS:
        try:
            value = getattr(patient, field_name)
        except AttributeError as exc:  # pragma: no cover
            raise ValueError(f"Patient has no attribute '{field_name}'") from exc
        context[field_name] = value

    # Render the template safely
    try:
        report = _render_template(template, context)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Template rendering error: {exc}") from exc

    return report

# --------------------------------------------------------------------------- #
# Example usage (remove or guard with `if __name__ == "__main__":` in real code)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Patient Report\n"
        "==============\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Diagnosis: {patient.diagnosis}\n"
        "Treatment Plan: {patient.treatment_plan}\n"
    )
    print(generate_user_report("12345", tmpl))