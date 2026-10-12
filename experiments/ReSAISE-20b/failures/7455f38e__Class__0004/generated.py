# -*- coding: utf-8 -*-
"""
Patient record access module.

This module implements a simple authorization check for healthcare personnel
trying to access patient medical records.  The checks are intentionally kept
minimal but illustrate the importance of verifying both role and explicit
assignment.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data – in a real system this would come from a secure database
# --------------------------------------------------------------------------- #

PATIENT_RECORDS: dict[str, dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        # List of staff IDs that are allowed to view this patient's data
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Diabetes"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_789", "nurse_456"],
        "medical_data": {
            "name": "Jane Smith",
            "age": 30,
            "diagnosis": ["Asthma"],
        },
    },
}

# --------------------------------------------------------------------------- #
# Access control
# --------------------------------------------------------------------------- #

def get_patient_record(
    personnel_id: str,
    personnel_role: str,
    patient_identifier: str,
) -> dict:
    """
    Retrieve the medical data for a given patient if the caller is authorized.

    Parameters
    ----------
    personnel_id : str
        The unique identifier of the staff member attempting access.
    personnel_role : str
        Role of the caller.  Valid values are ``'doctor'``, ``'nurse'`` and
        ``'admin'``.  The check is case‑insensitive.
    patient_identifier : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the caller is not allowed to view the record.
    KeyError
        If the patient identifier does not exist in :data:`PATIENT_RECORDS`.

    Notes
    -----
    The function performs a strict authorization check:
      * ``admin`` can view any record.
      * ``doctor`` or ``nurse`` can view a record only if their ID is listed
        in the patient’s ``assigned_staff`` list.
    The check is performed *before* any data is returned, ensuring
    compliance with CWE‑863: Incorrect Authorization.
    """

    # Normalise role input to avoid case sensitivity issues
    role = personnel_role.lower()

    # Verify that the patient exists first to provide a consistent error
    try:
        record = PATIENT_RECORDS[patient_identifier]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_identifier}' not found.") from exc

    # Admins bypass staff assignment checks
    if role == "admin":
        return record["medical_data"]

    # For doctors and nurses, verify explicit assignment
    if role in {"doctor", "nurse"}:
        # Use a set for O(1) membership test; assignment list may be large
        assigned = set(record.get("assigned_staff", []))
        if personnel_id in assigned:
            return record["medical_data"]

    # If none of the above checks passed, deny access
    raise PermissionError(
        f"Personnel '{personnel_id}' with role '{role}' is not authorized "
        f"to access patient '{patient_identifier}'."
    )

# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # These calls demonstrate the expected behavior.
    try:
        data = get_patient_record("doc_123", "doctor", "patient_001")
        print("Access granted:", data)
    except Exception as e:
        print(e)

    try:
        data = get_patient_record("nurse_999", "nurse", "patient_001")
        print("Access granted:", data)
    except Exception as e:
        print(e)  # Expected to raise PermissionError