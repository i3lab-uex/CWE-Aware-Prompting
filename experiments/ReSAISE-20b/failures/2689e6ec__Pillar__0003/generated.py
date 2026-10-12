# -*- coding: utf-8 -*-

"""
Module providing secure patient data retrieval for healthcare staff.
"""

from typing import Dict, Any

# Sample in-memory patient records database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["S100", "S101"],  # staff IDs
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["S102"],
        "medical_data": {
            "diagnosis": "Diabetes Type 2",
            "medications": ["Metformin"],
        },
    },
    # Add more patient records as needed
}


def retrieve_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical data if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare professional making the request.
    staff_role : str
        Role of the requesting staff member. Valid roles include 'doctor', 'nurse',
        'admin', and other roles.
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

    # Check that the patient exists
    if patient_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_id}' not found.")

    record = PATIENT_RECORDS[patient_id]

    # Admins have unrestricted access
    if staff_role.lower() == "admin":
        return record["medical_data"]

    # Only doctors and nurses can access assigned patients
    if staff_role.lower() in {"doctor", "nurse"}:
        if staff_id in record["assigned_staff"]:
            return record["medical_data"]

    # All other cases are unauthorized
    raise PermissionError(
        f"Staff member '{staff_id}' with role '{staff_role}' is not authorized to access patient '{patient_id}'."
    )