# -*- coding: utf-8 -*-

from typing import Dict, Any

# Example patient records database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril 10mg"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc789"],
        "medical_data": {
            "diagnosis": "Diabetes",
            "medications": ["Metformin 500mg"],
        },
    },
    # Add more patient records as needed
}

# Roles that are allowed to view any assigned patient's record
ALLOWED_ROLES = {"doctor", "nurse", "admin"}

def fetch_patient_record(staff_identifier: str, staff_role: str, patient_ident: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        The unique identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin', etc.).
    patient_ident : str
        The unique identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data dictionary.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to access the record.
    KeyError
        If the patient identifier is not found in PATIENT_RECORDS.
    """
    # Basic sanity checks on inputs
    if not isinstance(staff_identifier, str) or not staff_identifier.strip():
        raise ValueError("staff_identifier must be a non-empty string.")
    if not isinstance(staff_role, str) or not staff_role.strip():
        raise ValueError("staff_role must be a non-empty string.")
    if not isinstance(patient_ident, str) or not patient_ident.strip():
        raise ValueError("patient_ident must be a non-empty string.")

    # Retrieve the patient record; KeyError will propagate if not found
    patient_record = PATIENT_RECORDS[patient_ident]

    # Authorization logic: role must be allowed AND staff_identifier must be assigned
    is_role_allowed = staff_role.lower() in ALLOWED_ROLES
    is_staff_assigned = staff_identifier in patient_record.get("assigned_staff", [])

    if not (is_role_allowed and is_staff_assigned):
        raise PermissionError(
            f"Unauthorized access attempt by staff '{staff_identifier}' "
            f"with role '{staff_role}' to patient '{patient_ident}'."
        )

    # Return a copy to prevent accidental mutation of the original data
    return dict(patient_record["medical_data"])