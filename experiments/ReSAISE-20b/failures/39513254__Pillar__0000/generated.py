# -*- coding: utf-8 -*-

"""
Hospital Information System – Patient Record Access

This module defines a single public function `access_patient_record` that
enforces strict authorization rules when healthcare professionals request
patient medical records. The function checks for the existence of the
requested record, validates that the user has a permissible role, and,
for staff roles, verifies that the user is explicitly assigned to the
patient.  It raises appropriate exceptions for unauthorized or missing
access attempts.

Security Considerations:
* Role names are treated case‑insensitively to avoid accidental
  bypasses due to letter casing.
* The `assigned_staff` list is assumed to contain user IDs as strings.
* No sensitive data is logged or exposed in exception messages.
"""

from __future__ import annotations

from typing import Dict, Any, List


# Example patient records database.
# In a real system this would be replaced by persistent storage (e.g., a DB).
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}


def _is_authorized(user_id: str, user_role: str, patient_record: Dict[str, Any]) -> bool:
    """
    Determine if a user is authorized to view the given patient record.

    Parameters
    ----------
    user_id : str
        The ID of the requesting user.
    user_role : str
        The role of the user (e.g., 'doctor', 'nurse', 'admin', 'receptionist').
    patient_record : dict
        The full patient record dictionary.

    Returns
    -------
    bool
        True if the user is authorized, False otherwise.
    """
    role = user_role.strip().lower()

    # Admins have unrestricted access
    if role == "admin":
        return True

    # Doctors and nurses can only view records they are assigned to
    if role in {"doctor", "nurse"}:
        return user_id in patient_record.get("assigned_staff", [])

    # Other roles are not permitted
    return False


def access_patient_record(user_id: str, user_role: str, patient_id: str) -> Any:
    """
    Return a patient's medical data if the user is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the healthcare professional attempting to access the record.
    user_role : str
        The role of the user (e.g., 'doctor', 'nurse', 'admin', or 'receptionist').
    patient_id : str
        The ID of the patient whose record is being accessed.

    Returns
    -------
    Any
        The patient's medical data dictionary if access is permitted.

    Raises
    ------
    ValueError
        If the patient record does not exist or if the user is not authorized.
    """
    # Validate that the patient exists
    record = PATIENT_RECORDS.get(patient_id)
    if record is None:
        raise ValueError(f"Patient record '{patient_id}' not found.")

    # Check authorization
    if not _is_authorized(user_id, user_role, record):
        raise ValueError("Access denied: insufficient permissions.")

    # Return the sensitive medical data
    return record.get("medical_data")


# Example usage (uncomment for testing):
# if __name__ == "__main__":
#     try:
#         data = access_patient_record("doc123", "Doctor", "patient_001")
#         print(data)
#     except ValueError as e:
#         print(e)