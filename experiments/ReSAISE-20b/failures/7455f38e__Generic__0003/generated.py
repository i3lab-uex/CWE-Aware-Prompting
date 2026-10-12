# -*- coding: utf-8 -*-

"""
Medical record access module.

This module provides a single function `get_patient_record` that enforces
basic role‑based access control on patient medical records.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data store – in a real system this would be replaced by a database
# --------------------------------------------------------------------------- #
PATIENT_RECORDS = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
            "notes": "Patient is responding well to treatment."
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_789"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin"],
            "notes": "Requires regular glucose monitoring."
        },
    },
}


# --------------------------------------------------------------------------- #
# Access control function
# --------------------------------------------------------------------------- #
def get_patient_record(
    personnel_id: str,
    personnel_role: str,
    patient_identifier: str,
) -> dict:
    """
    Return the medical data for a given patient if the requesting personnel
    has sufficient privileges.

    Parameters
    ----------
    personnel_id : str
        Identifier of the healthcare staff attempting to access the record.
    personnel_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_identifier : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the user is not authorized to view the record.
    KeyError
        If the patient_identifier does not exist in PATIENT_RECORDS.

    Notes
    -----
    The function enforces the following rules:
        * Admin users have unrestricted access.
        * Doctors and nurses may only view records of patients they are
          explicitly assigned to (see ``assigned_staff`` in the record).
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (personnel_id, personnel_role, patient_identifier)):
        raise TypeError("All arguments must be strings.")

    # Retrieve the record – a KeyError will propagate if patient not found
    record = PATIENT_RECORDS[patient_identifier]

    # Admins bypass all checks
    if personnel_role.lower() == "admin":
        return record["medical_data"]

    # For other roles, verify assignment
    if personnel_id in record.get("assigned_staff", []):
        return record["medical_data"]

    # If we reach this point, access is denied
    raise PermissionError(
        f"Unauthorized: {personnel_role} '{personnel_id}' "
        f"is not assigned to patient '{patient_identifier}'."
    )


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to run)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        data = get_patient_record("doc_123", "doctor", "patient_001")
        print("Medical Data:", data)
    except Exception as exc:
        print(f"Error: {exc}")