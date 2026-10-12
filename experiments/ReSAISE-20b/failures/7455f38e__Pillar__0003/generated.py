# -*- coding: utf-8 -*-
"""
Patient record access module.

This module defines a secure function `get_patient_record` that checks
authorization before returning sensitive medical data.  The function
prevents CWE‑284 (Improper Access Control) by ensuring that only
authorized personnel can retrieve a patient’s records.
"""

from __future__ import annotations

# Sample data structure; in production this would be loaded from a secure DB
PATIENT_RECORDS: dict[str, dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_789", "nurse_456"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Roles that are allowed to view any patient record
ALLOWED_ROLES = {"doctor", "nurse", "admin"}

def get_patient_record(
    personnel_id: str,
    personnel_role: str,
    patient_identifier: str,
) -> dict:
    """
    Return a patient's medical data if the requesting personnel is authorized.

    Parameters
    ----------
    personnel_id : str
        The unique identifier of the healthcare staff member.
    personnel_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_identifier : str
        The unique identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the personnel is not authorized to access the requested record.
    KeyError
        If the patient identifier does not exist in `PATIENT_RECORDS`.
    """

    # Validate that the patient exists
    if patient_identifier not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_identifier}' not found.")

    record = PATIENT_RECORDS[patient_identifier]

    # Check role-based permission
    if personnel_role not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{personnel_role}' is not authorized to access patient records."
        )

    # Check staff assignment
    if personnel_id not in record["assigned_staff"]:
        raise PermissionError(
            f"Personnel ID '{personnel_id}' is not assigned to patient "
            f"'{patient_identifier}'."
        )

    # All checks passed; return medical data
    return record["medical_data"]


# Example usage (commented out for safety)
# if __name__ == "__main__":
#     try:
#         data = get_patient_record("doc_123", "doctor", "patient_001")
#         print(data)
#     except Exception as e:
#         print(f"Access denied: {e}")