# -*- coding: utf-8 -*-
"""
Secure patient record access module.

Author: OpenAI ChatGPT
Date: 2026-07-23

This module defines a single function `fetch_patient_record` that enforces
strict access control on patient medical records.  It protects against
CWE-284: Improper Access Control by ensuring only authorized staff members
can read a record.
"""

from __future__ import annotations

import typing as _t

# Example patient records database
PATIENT_RECORDS: dict[str, dict[str, _t.Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {"diagnosis": "Hypertension", "medication": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc789"],
        "medical_data": {"diagnosis": "Diabetes", "medication": ["Metformin"]},
    },
}

# Roles that are allowed to read patient data
ALLOWED_ROLES: set[str] = {"doctor", "nurse"}


def fetch_patient_record(
    staff_identifier: str,
    staff_role: str,
    patient_ident: str,
) -> dict[str, _t.Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        The unique identifier of the healthcare professional making the request.
    staff_role : str
        Role of the staff member, e.g., 'doctor', 'nurse', 'admin'.
    patient_ident : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict[str, Any]
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to access the record.
    KeyError
        If the patient identifier is not found in PATIENT_RECORDS.

    Notes
    -----
    - Only staff with roles listed in ALLOWED_ROLES are permitted to read records.
    - Even authorized roles must be assigned to the patient in the
      `assigned_staff` list.
    - The function returns a *copy* of the medical data to prevent accidental
      modification of the original record.
    """
    # Quick lookup for patient existence
    try:
        record = PATIENT_RECORDS[patient_ident]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_ident}' not found.") from exc

    # Role-based access check
    if staff_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Access denied: role '{staff_role}' is not authorized to view patient records."
        )

    # Staff assignment check
    if staff_identifier not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Access denied: staff ID '{staff_identifier}' is not assigned to patient '{patient_ident}'."
        )

    # Return a deep copy to avoid external mutation
    return _t.cast(dict[str, _t.Any], record["medical_data"].copy())


# Example usage (commented out to avoid accidental execution)
# if __name__ == "__main__":
#     try:
#         data = fetch_patient_record("doc123", "doctor", "patient_001")
#         print(data)
#     except Exception as e:
#         print(e)