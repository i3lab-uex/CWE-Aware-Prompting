# -*- coding: utf-8 -*-

"""
Utility to retrieve patient data with proper authorization checks.
"""

from typing import Dict, Any

# Example patient records (this would normally be imported from a secure data store)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": {"D123", "N456"},
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": "Hypertension",
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": {"D789"},
        "medical_data": {
            "name": "Jane Smith",
            "age": 30,
            "diagnosis": "Asthma",
        },
    },
    # ... more records ...
}


def retrieve_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a given patient if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to access the patient's data.
    KeyError
        If the patient_id does not exist in PATIENT_RECORDS.
    """
    # Normalise inputs to avoid accidental mismatches
    staff_id = staff_id.strip()
    staff_role = staff_role.strip().lower()
    patient_id = patient_id.strip()

    # 1. Verify that the patient exists
    if patient_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_id}' not found.")

    patient_record = PATIENT_RECORDS[patient_id]
    assigned_staff: set[str] = patient_record.get("assigned_staff", set())

    # 2. Authorization logic
    authorized = False

    if staff_role == "admin":
        # Admins can access any record
        authorized = True

    elif staff_role in {"doctor", "nurse"}:
        # Doctors and nurses can access only if assigned to the patient
        authorized = staff_id in assigned_staff

    else:
        # Other roles (e.g., receptionist) are not allowed to access medical data
        authorized = False

    # 3. Enforce the check (CWE-863 prevention)
    if not authorized:
        raise PermissionError(
            f"Access denied: staff '{staff_id}' with role '{staff_role}' "
            f"is not authorized to view patient '{patient_id}'."
        )

    # 4. Return a copy of medical data to prevent accidental mutation
    return dict(patient_record.get("medical_data", {}))