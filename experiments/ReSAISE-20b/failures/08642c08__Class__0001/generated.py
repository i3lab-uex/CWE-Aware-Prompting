# -*- coding: utf-8 -*-

"""
Module providing patient data access with proper authorization checks.
"""

from typing import Dict, List, Any

# Example patient records database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_789"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin"],
        },
    },
}


def fetch_patient_info(
    staff_identifier: str,
    staff_role: str,
    patient_ref: str,
) -> Dict[str, Any]:
    """
    Retrieve medical data for a specified patient if the staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        Unique identifier for the healthcare staff member attempting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        Identifier of the patient whose records are being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    KeyError
        If the patient_ref does not exist in PATIENT_RECORDS.
    PermissionError
        If the staff member is not authorized to access the patient's data.
    """
    # Ensure patient exists
    if patient_ref not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_ref}' not found.")

    patient_record = PATIENT_RECORDS[patient_ref]

    # Authorization logic
    is_admin = staff_role.lower() == "admin"
    is_assigned = staff_identifier in patient_record.get("assigned_staff", [])

    if not (is_admin or is_assigned):
        raise PermissionError(
            f"Unauthorized access: staff '{staff_identifier}' "
            f"with role '{staff_role}' cannot view patient '{patient_ref}'."
        )

    # Return a copy to prevent accidental mutation of the internal data
    return dict(patient_record.get("medical_data", {}))