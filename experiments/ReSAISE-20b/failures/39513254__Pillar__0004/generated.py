# -*- coding: utf-8 -*-

from typing import Dict, Any

# Sample patient records database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["U100", "U101"],  # doctor and nurse IDs
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Amlodipine"]},
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["U102"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}


def access_patient_record(user_id: str, user_role: str, patient_id: str) -> Any:
    """
    Allow a healthcare professional to access a patient's medical record
    after performing proper authorization checks.

    Parameters
    ----------
    user_id : str
        The ID of the healthcare professional attempting to access the record.
    user_role : str
        The role of the user (e.g., 'doctor', 'nurse', 'admin', or 'receptionist').
    patient_id : str
        The ID of the patient whose record is being accessed.

    Returns
    -------
    Any
        The patient's medical data if the user is authorized.

    Raises
    ------
    ValueError
        If the patient record does not exist.
    """
    # 1. Validate that the patient exists
    record = PATIENT_RECORDS.get(patient_id)
    if record is None:
        raise ValueError(f"Patient record with ID '{patient_id}' does not exist.")

    # 2. Authorization logic
    # Admins can access any record
    if user_role.lower() == "admin":
        return record["medical_data"]

    # Doctors and nurses can access only if they are assigned to the patient
    if user_role.lower() in {"doctor", "nurse"}:
        if user_id in record.get("assigned_staff", []):
            return record["medical_data"]

    # Receptionists and any other roles are not permitted to view medical data
    return "Authorization error"