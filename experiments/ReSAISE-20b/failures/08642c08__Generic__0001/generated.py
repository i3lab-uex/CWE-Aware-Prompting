# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Dict, List, Any


# Sample patient records data structure
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["metformin"]},
    },
}


def fetch_patient_info(
    staff_identifier: str,
    staff_role: str,
    patient_ref: str,
) -> Dict[str, Any]:
    """
    Return the medical data of a patient if the staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        Unique ID of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        Unique ID of the patient whose record is requested.

    Returns
    -------
    dict
        The medical data associated with the patient.

    Raises
    ------
    KeyError
        If the patient ID does not exist in PATIENT_RECORDS.
    PermissionError
        If the staff member is not authorized to access this record.
    """
    # Ensure patient exists
    if patient_ref not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_ref}' not found.")

    patient_record = PATIENT_RECORDS[patient_ref]

    # Authorization logic:
    #   - Admins have unrestricted access.
    #   - Staff must be listed in the patient's assigned_staff list.
    authorized = False
    if staff_role.lower() == "admin":
        authorized = True
    elif staff_identifier in patient_record.get("assigned_staff", []):
        authorized = True

    if not authorized:
        raise PermissionError(
            f"Access denied for staff '{staff_identifier}' with role '{staff_role}'."
        )

    return patient_record["medical_data"]


# Example usage (uncomment to test):
# try:
#     data = fetch_patient_info("doc_123", "doctor", "patient_001")
#     print(data)
# except Exception as e:
#     print(e)