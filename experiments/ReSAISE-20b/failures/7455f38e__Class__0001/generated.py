#!/usr/bin/env python3
"""
Medical record access module.

This module defines the `get_patient_record` function, which enforces
strict authorization checks before exposing sensitive patient data.
"""

from __future__ import annotations

import copy
from typing import Dict, List, Any


# ----------------------------------------------------------------------
# Sample patient records database.
#
# In a real system this would be replaced by a secure persistence layer
# (e.g., an encrypted database).  The data structure below is only for
# demonstration purposes.
# ----------------------------------------------------------------------
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        # List of personnel IDs that are explicitly authorized to view this record.
        "assigned_staff": ["doc_123", "nurse_456"],
        # Sensitive medical data.  In practice this would be encrypted.
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
            "notes": "Patient advised to reduce sodium intake."
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_789"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin"],
            "notes": "Schedule HbA1c test in 3 months."
        },
    },
}


# ----------------------------------------------------------------------
# Authorization helper
# ----------------------------------------------------------------------
def _is_authorized(
    personnel_id: str,
    personnel_role: str,
    patient_record: Dict[str, Any],
) -> bool:
    """
    Determine whether the personnel is authorized to access the given patient record.

    Rules:
        * An 'admin' may view any record.
        * A staff member must be listed in the patient's `assigned_staff`.
    """
    # Normalize role to lower-case to avoid case-sensitive mismatches.
    normalized_role = personnel_role.strip().lower()

    if normalized_role == "admin":
        return True

    # Exact membership check; no wildcards or substring matching.
    return personnel_id in patient_record.get("assigned_staff", [])


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def get_patient_record(
    personnel_id: str,
    personnel_role: str,
    patient_identifier: str,
) -> Dict[str, Any]:
    """
    Return the medical data for a patient if the caller is authorized.

    Parameters
    ----------
    personnel_id : str
        Identifier of the healthcare staff attempting access.
    personnel_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_identifier : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    Dict[str, Any]
        A deep copy of the patient's medical data.

    Raises
    ------
    KeyError
        If the patient_identifier does not exist in PATIENT_RECORDS.
    PermissionError
        If the personnel is not authorized to view the record.
    """
    # Validate input types early
    if not isinstance(personnel_id, str):
        raise TypeError("personnel_id must be a string")
    if not isinstance(personnel_role, str):
        raise TypeError("personnel_role must be a string")
    if not isinstance(patient_identifier, str):
        raise TypeError("patient_identifier must be a string")

    # Retrieve the patient record; raise KeyError if missing.
    try:
        patient_record = PATIENT_RECORDS[patient_identifier]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_identifier}' not found") from exc

    # Perform authorization check
    if not _is_authorized(personnel_id, personnel_role, patient_record):
        raise PermissionError(
            f"Personnel '{personnel_id}' with role '{personnel_role}' "
            "is not authorized to access this patient record."
        )

    # Return a deep copy to prevent accidental mutation of the stored data.
    return copy.deepcopy(patient_record["medical_data"])


# ----------------------------------------------------------------------
# Example usage (for demonstration; remove or guard in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        record = get_patient_record("doc_123", "doctor", "patient_001")
        print("Access granted. Medical data:")
        print(record)
    except Exception as e:
        print(f"Error: {e}")