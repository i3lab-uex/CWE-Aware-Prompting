# -*- coding: utf-8 -*-
"""
Hospital Information System – Patient Record Access Module

This module provides a single function `access_patient_record` that
enforces fine‑grained authorization checks before exposing medical data.
"""

from typing import Dict, Any

# Example patient records. In a real system this would be retrieved from
# a secure database rather than hard‑coded.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": {"doctor_123", "nurse_456"},
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    # Additional patient records would be added here.
}


def access_patient_record(user_id: str, user_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Return a patient's medical data if the requesting user is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the healthcare professional attempting to access the record.
    user_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin', or 'receptionist').
    patient_id : str
        The ID of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    ValueError
        If the patient record does not exist.
    PermissionError
        If the user is not authorized to access the requested record.
    """
    # 1. Validate patient existence
    record = PATIENT_RECORDS.get(patient_id)
    if record is None:
        raise ValueError(f"Patient record '{patient_id}' does not exist.")

    # 2. Authorization logic
    # Admins have blanket access to all records.
    if user_role.lower() == "admin":
        return record["medical_data"]

    # Doctors and nurses may only access records where they are explicitly assigned.
    if user_role.lower() in {"doctor", "nurse"}:
        if user_id in record["assigned_staff"]:
            return record["medical_data"]

    # All other roles (e.g., receptionist) are denied access.
    raise PermissionError(
        f"User '{user_id}' with role '{user_role}' is not authorized to access patient record '{patient_id}'."
    )