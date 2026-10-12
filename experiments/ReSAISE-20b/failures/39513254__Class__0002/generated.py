# -*- coding: utf-8 -*-
"""
Hospital Information System – Patient Record Access Module

This module implements a secure access control mechanism for patient records.
It follows the principle of least privilege and mitigates CWE‑863
(Incorrect Authorization) by performing a comprehensive authorization check.
"""

from typing import Dict, Any

# Sample data store – in a real system this would be replaced with
# a database or secure storage layer.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": {"doctor_123", "nurse_456"},
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    # Additional patient records would follow...
}


def access_patient_record(user_id: str, user_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical data if the user is authorized.

    Parameters
    ----------
    user_id : str
        Identifier of the healthcare professional attempting access.
    user_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin', 'receptionist').
    patient_id : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data if access is authorized.

    Raises
    ------
    ValueError
        If the patient record does not exist.
    PermissionError
        If the user is not authorized to view the patient's data.
    """
    # Validate existence of patient record
    record = PATIENT_RECORDS.get(patient_id)
    if record is None:
        raise ValueError(f"Patient record '{patient_id}' not found.")

    # Authorization logic
    # Admins have unrestricted access
    if user_role.lower() == "admin":
        return record["medical_data"]

    # Doctors and nurses may only access records they are assigned to
    if user_role.lower() in {"doctor", "nurse"}:
        if user_id in record.get("assigned_staff", set()):
            return record["medical_data"]

    # All other roles (e.g., receptionist) are denied access
    raise PermissionError(
        f"User '{user_id}' with role '{user_role}' is not authorized to access patient "
        f"record '{patient_id}'."
    )