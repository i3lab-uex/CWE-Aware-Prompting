# -*- coding: utf-8 -*-
"""
Healthcare patient record retrieval module.

Provides a single function `retrieve_patient_data` that validates
authorization before returning sensitive medical information.
"""

from __future__ import annotations

from typing import Dict, Any, List

# Example patient records database.
# In a real system this would be replaced by a secure persistent store.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        # List of staff IDs who have explicit access to this record
        "assigned_staff": ["doc_123", "nurse_456"],
        # The actual medical data (redacted in this example)
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Roles that are allowed to view patient records.
ALLOWED_ROLES: List[str] = ["doctor", "nurse", "admin"]


def retrieve_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Any:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare professional making the request.
    staff_role : str
        Role of the requesting staff member (e.g., 'doctor', 'nurse', 'admin',
        or other roles such as 'receptionist').
    patient_id : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    Any
        The medical data associated with the patient record.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient_id is not found in PATIENT_RECORDS.

    Notes
    -----
    - Only staff with a role listed in `ALLOWED_ROLES` and who are
      explicitly assigned to the patient record may access it.
    - The function performs minimal validation; in production, further checks
      (e.g., session authentication, audit logging) would be required.
    """
    # Validate patient existence
    if patient_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_id}' does not exist.")

    record = PATIENT_RECORDS[patient_id]

    # Check role-based permission
    if staff_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Access denied: role '{staff_role}' is not authorized to view patient records."
        )

    # Check staff assignment
    if staff_id not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Access denied: staff ID '{staff_id}' is not assigned to patient '{patient_id}'."
        )

    # All checks passed; return the medical data
    return record["medical_data"]


# Example usage (uncomment to test):
# try:
#     data = retrieve_patient_data("doc_123", "doctor", "patient_001")
#     print(data)
# except Exception as e:
#     print(e)