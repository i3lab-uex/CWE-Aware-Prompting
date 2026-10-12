#!/usr/bin/env python3
"""
Secure patient record retrieval with proper authorization checks.
"""

from typing import Dict, List

# Example data store. In production this would be a secure database.
PATIENT_RECORDS: Dict[str, Dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": [
            {"id": "dr_smith", "role": "doctor"},
            {"id": "nurse_jane", "role": "nurse"}
        ],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Monitor blood pressure daily."
        }
    },
    # Add more patient records as needed
}


def get_patient_record(
    personnel_id: str,
    personnel_role: str,
    patient_identifier: str
) -> Dict:
    """
    Retrieve a patient's medical data if the requesting personnel is authorized.

    Parameters
    ----------
    personnel_id : str
        Identifier of the healthcare staff attempting access.
    personnel_role : str
        Role of the requesting staff (e.g., 'doctor', 'nurse', 'admin').
    patient_identifier : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    Dict
        The patient's medical data dictionary.

    Raises
    ------
    PermissionError
        If the personnel is not authorized to access the record.
    KeyError
        If the patient_identifier does not exist in PATIENT_RECORDS.
    """
    # Validate that the patient exists
    if patient_identifier not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_identifier}' not found.")

    record = PATIENT_RECORDS[patient_identifier]
    assigned_staff: List[Dict[str, str]] = record.get("assigned_staff", [])

    # Authorization check: personnel must be listed in assigned_staff
    # and their role must match the stored role.
    authorized = any(
        staff["id"] == personnel_id and staff["role"].lower() == personnel_role.lower()
        for staff in assigned_staff
    )

    if not authorized:
        raise PermissionError(
            f"Personnel '{personnel_id}' with role '{personnel_role}' "
            "is not authorized to access this patient's record."
        )

    # Return a copy to prevent accidental mutation of the stored data.
    return dict(record.get("medical_data", {}))