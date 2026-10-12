# -*- coding: utf-8 -*-

"""
Secure patient data access module.

Author: Your Name
"""

from typing import Dict, Any

# Example patient records database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_123", "staff_456"],  # staff IDs
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
            "notes": "Monitor blood pressure daily."
        }
    },
    # Add more patient records as needed.
}


def get_patient_data(staff_num: str, role: str, patient_ref: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_num : str
        Identifier of the healthcare professional requesting access.
    role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin', 'receptionist').
    patient_ref : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    KeyError
        If the patient reference does not exist in PATIENT_RECORDS.
    PermissionError
        If the staff member is not authorized to view the record.
    """
    # Validate that patient exists
    if patient_ref not in PATIENT_RECORDS:
        raise KeyError(f"Patient reference '{patient_ref}' not found.")

    record = PATIENT_RECORDS[patient_ref]

    # Define which roles are automatically allowed to access any record
    ALLOWED_ROLES = {"doctor", "nurse", "admin"}

    # Check role-based access
    if role.lower() in ALLOWED_ROLES:
        return record["medical_data"]

    # If role is not automatically allowed, check staff assignment
    if staff_num in record.get("assigned_staff", []):
        return record["medical_data"]

    # If neither condition met, deny access
    raise PermissionError(
        f"Access denied: staff '{staff_num}' with role '{role}' "
        f"is not authorized to view patient '{patient_ref}'."
    )