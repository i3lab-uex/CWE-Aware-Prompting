# -*- coding: utf-8 -*-
"""
Patient data review module.

Provides a single function `review_patient_data` that enforces basic
access control for healthcare staff.  Staff may only view a patient's
medical data if they are either:
    • an administrator, or
    • explicitly listed in the patient's `assigned_staff` list.
"""

from __future__ import annotations

from typing import Dict, List, Any


# Example patient records database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_a", "nurse_b"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    # Add more patient records here...
}


def review_patient_data(
    staff_id: str,
    staff_role: str,
    patient_id: str,
) -> Dict[str, Any]:
    """
    Return a patient's medical data if the requesting staff member has
    sufficient permissions.

    Parameters
    ----------
    staff_id : str
        Identifier for the healthcare personnel requesting access.
    staff_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier for the target patient.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member does not have access to the patient's data.
    KeyError
        If the patient_id is not present in PATIENT_RECORDS.
    """
    # Validate that the patient exists
    if patient_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_id}' not found.")

    patient_record = PATIENT_RECORDS[patient_id]

    # Admins have blanket access
    if staff_role.lower() == "admin":
        return patient_record["medical_data"]

    # Check explicit assignment
    if staff_id in patient_record.get("assigned_staff", []):
        return patient_record["medical_data"]

    # If we reach here, access is denied
    raise PermissionError(
        f"Staff member '{staff_id}' with role '{staff_role}' is not authorized "
        f"to access patient '{patient_id}'."
    )