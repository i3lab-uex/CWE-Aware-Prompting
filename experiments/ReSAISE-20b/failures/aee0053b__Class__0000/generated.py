# -*- coding: utf-8 -*-
"""
Secure patient record retrieval.

The function enforces strict authorization by checking that the requesting staff
identifier is listed among the assigned staff for the patient and that the role
belongs to an approved set of roles.  It raises a PermissionError if either check fails.
"""

from typing import Dict, Any

# Example patient records database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": {"S100", "S101"},  # staff IDs assigned to this patient
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": {"S102"},
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
    # ... more patient records ...
}

# Set of roles that are permitted to view medical data
ALLOWED_ROLES = {"doctor", "nurse", "admin"}


def get_patient_data(staff_num: str, role: str, patient_ref: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a patient if the requesting staff member is authorized.

    Parameters
    ----------
    staff_num : str
        Identifier of the healthcare professional requesting access.
    role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    KeyError
        If the patient reference does not exist in PATIENT_RECORDS.
    PermissionError
        If the staff member is not authorized to access this record.
    """
    # Retrieve patient record; KeyError will propagate if patient_ref is invalid
    patient_record = PATIENT_RECORDS[patient_ref]

    # Authorization checks (CWE-863 mitigation)
    # 1. Check role membership first
    if role not in ALLOWED_ROLES:
        raise PermissionError(f"Role '{role}' is not authorized to access patient records.")

    # 2. Check staff assignment
    if staff_num not in patient_record["assigned_staff"]:
        raise PermissionError(
            f"Staff member '{staff_num}' is not assigned to patient '{patient_ref}'."
        )

    # All checks passed; return medical data
    return patient_record["medical_data"]