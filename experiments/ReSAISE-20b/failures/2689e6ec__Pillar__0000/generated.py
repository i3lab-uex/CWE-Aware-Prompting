# -*- coding: utf-8 -*-
"""
Utility to retrieve a patient's medical record for authorized staff.

Author: <Your Name>
"""

from typing import Dict, Any

# Example patient records. In production this would come from a secure database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    # Add more patient records as needed.
}


def retrieve_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin', etc.).
    patient_id : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    KeyError
        If the patient_id is not found in PATIENT_RECORDS.
    PermissionError
        If the staff member does not have permission to access the record.
    """
    # Validate patient exists
    if patient_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_id}' does not exist.")

    record = PATIENT_RECORDS[patient_id]

    # Authorization logic
    authorized_roles = {"doctor", "nurse", "admin"}
    if staff_role not in authorized_roles:
        raise PermissionError(
            f"Staff role '{staff_role}' is not permitted to access patient records."
        )

    # Admins have blanket access
    if staff_role == "admin":
        return record["medical_data"]

    # For doctors and nurses, check if they are assigned to this patient
    if staff_id not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Staff member '{staff_id}' is not assigned to patient '{patient_id}'."
        )

    return record["medical_data"]