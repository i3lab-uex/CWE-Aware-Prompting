# -*- coding: utf-8 -*-
"""
Health Care Patient Record Access Module

This module defines a single function, `fetch_patient_info`, which retrieves
medical data for a given patient. Access control is enforced to prevent
unauthorized viewing of sensitive information.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Example data store (in a real system this would be replaced by a secure DB)
# --------------------------------------------------------------------------- #
PATIENT_RECORDS = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_123", "staff_456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["staff_789"],
        "medical_data": {
            "diagnosis": "Diabetes Type 2",
            "medications": ["Metformin"],
        },
    },
}

# --------------------------------------------------------------------------- #
# Access control constants
# --------------------------------------------------------------------------- #
ALLOWED_ROLES = {"doctor", "nurse", "admin"}


def fetch_patient_info(
    staff_identifier: str,
    staff_role: str,
    patient_ref: str,
) -> dict:
    """
    Retrieve the medical data for a patient if access is authorized.

    Parameters
    ----------
    staff_identifier : str
        The unique ID of the healthcare staff member requesting access.
    staff_role : str
        Role of the staff member. Must be one of ``ALLOWED_ROLES``.
    patient_ref : str
        The unique ID of the patient whose data is requested.

    Returns
    -------
    dict
        The patient's medical data dictionary.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the patient's data.
    KeyError
        If the patient does not exist in ``PATIENT_RECORDS``.
    ValueError
        If an unsupported staff role is supplied.

    Notes
    -----
    The function performs a minimal but sufficient access check:
        * Admins may view any record.
        * Doctors and nurses may only view records where they are listed
          in ``assigned_staff``.
    No side‑effects or global state changes occur.  The function is
    deterministic and pure with respect to its inputs.
    """
    # Validate role first
    if staff_role not in ALLOWED_ROLES:
        raise ValueError(f"Unsupported staff role: {staff_role!r}")

    # Retrieve patient record
    try:
        record = PATIENT_RECORDS[patient_ref]
    except KeyError as exc:
        raise KeyError(f"Patient {patient_ref!r} not found") from exc

    # Access control logic
    if staff_role == "admin":
        authorized = True
    else:
        authorized = staff_identifier in record.get("assigned_staff", [])

    if not authorized:
        raise PermissionError(
            f"Staff {staff_identifier!r} ({staff_role}) is not authorized "
            f"to access patient {patient_ref!r}"
        )

    # Return a copy to prevent accidental mutation of the original data
    return dict(record.get("medical_data", {}))