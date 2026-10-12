# -*- coding: utf-8 -*-
"""
Module providing secure access to patient records.
"""

from typing import Dict, Any

# Example data structure; in practice this would be loaded from a secure database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Type II Diabetes"],
            "medications": ["Lisinopril", "Metformin"],
        },
    },
    # Additional patient records would follow...
}


def get_patient_record(
    personnel_id: str,
    personnel_role: str,
    patient_identifier: str,
) -> Dict[str, Any]:
    """
    Retrieve the medical data for a patient if access is authorized.

    Parameters
    ----------
    personnel_id : str
        Identifier of the healthcare staff requesting access.
    personnel_role : str
        Role of the requester (e.g., 'doctor', 'nurse', 'admin').
    patient_identifier : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The medical data for the specified patient.

    Raises
    ------
    PermissionError
        If the requester does not have permission to view the record.
    KeyError
        If the patient identifier is unknown.

    Notes
    -----
    - An administrator (role == 'admin') may access any record.
    - For non-admin roles, the requester must be listed in the patient's
      ``assigned_staff`` list.
    - The function is intentionally conservative to avoid accidental data leaks.
    """
    # Validate that the patient exists
    try:
        record = PATIENT_RECORDS[patient_identifier]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_identifier}' not found.") from exc

    # Admins bypass staff assignment checks
    if personnel_role.lower() == "admin":
        return record["medical_data"]

    # Non-admins must be explicitly assigned
    if personnel_id not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Access denied: personnel '{personnel_id}' "
            f"is not assigned to patient '{patient_identifier}'."
        )

    return record["medical_data"]