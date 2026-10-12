# -*- coding: utf-8 -*-
"""
Module providing controlled access to patient medical records.
"""

from __future__ import annotations

# Sample data store – in a real system this would be backed by a secure database.
PATIENT_RECORDS = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc789"],
        "medical_data": {
            "diagnosis": "Diabetes",
            "medications": ["Metformin"],
        },
    },
}

# Roles that are allowed to access patient data.
ALLOWED_ROLES = {"doctor", "nurse", "admin"}


def fetch_patient_info(staff_identifier: str, staff_role: str, patient_ref: str):
    """
    Retrieve medical data for a patient if the requesting staff member has
    appropriate permissions.

    Parameters
    ----------
    staff_identifier : str
        Unique identifier of the healthcare personnel requesting access.
    staff_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        Identifier of the patient whose records are requested.

    Returns
    -------
    dict
        The patient's medical data if access is granted.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient identifier is not found in `PATIENT_RECORDS`.
    """
    # Validate role first – if the role is not recognized, deny access outright.
    if staff_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{staff_role}' is not authorized to access patient data."
        )

    # Fetch the patient record – raise KeyError if missing (handled by caller).
    try:
        record = PATIENT_RECORDS[patient_ref]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_ref}' not found.") from exc

    # Check if the staff member is explicitly assigned to this patient.
    if staff_identifier not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Staff member '{staff_identifier}' is not assigned to patient '{patient_ref}'."
        )

    # Access granted – return a copy to prevent accidental mutation.
    return dict(record.get("medical_data", {}))