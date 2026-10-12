# -*- coding: utf-8 -*-
"""
Implementation of a simple patient data retrieval API with proper access control.

Author: OpenAI ChatGPT
"""

from typing import Dict, Any

# Example patient records dictionary. In a real system this would come from
# a secure database or an external service.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Amlodipine"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Roles that are globally allowed to access any patient record
GLOBAL_ROLES = {"admin"}

def retrieve_patient_data(
    staff_id: str,
    staff_role: str,
    patient_id: str
) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record for an authorized staff member.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the professional (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data dictionary.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to access the requested record.
    KeyError
        If the patient_id does not exist in PATIENT_RECORDS.
    """
    # Ensure the patient record exists
    if patient_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_id}' not found.")

    record = PATIENT_RECORDS[patient_id]

    # Global role check: admins can access any patient record
    if staff_role.lower() in GLOBAL_ROLES:
        return record["medical_data"]

    # Check that the staff member is explicitly assigned to this patient
    if staff_id not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Access denied for staff_id '{staff_id}' with role '{staff_role}'. "
            "You are not assigned to this patient."
        )

    # If we reach here, the staff member is authorized
    return record["medical_data"]