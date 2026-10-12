# -*- coding: utf-8 -*-
"""
A simple access‑controlled patient record retrieval module.
"""

from typing import Dict, Any

# Sample in‑memory database of patient records
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": {"E1001", "E1002"},  # staff IDs allowed to view
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Type II Diabetes"],
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": {"E1003"},
        "medical_data": {
            "name": "Jane Smith",
            "age": 30,
            "diagnosis": ["Asthma"],
        },
    },
    # ... more records ...
}

# Roles that are always granted access regardless of assignment
ALLOWED_ROLES = {"doctor", "nurse", "admin"}


def retrieve_patient_data(employee_id: str, employee_role: str, patient_code: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record after performing an access control check.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the healthcare professional requesting access.
    employee_role : str
        Role of the employee (e.g., 'doctor', 'nurse', 'admin').
    patient_code : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data if access is authorized.

    Raises
    ------
    KeyError
        If the patient_code does not exist in PATIENT_RECORDS.
    PermissionError
        If the employee is not authorized to view the patient's record.
    """

    # Basic validation of inputs
    if not isinstance(employee_id, str) or not employee_id.strip():
        raise ValueError("employee_id must be a non‑empty string")
    if not isinstance(employee_role, str) or not employee_role.strip():
        raise ValueError("employee_role must be a non‑empty string")
    if not isinstance(patient_code, str) or not patient_code.strip():
        raise ValueError("patient_code must be a non‑empty string")

    # Fetch the patient record; KeyError will propagate if not found
    patient_record = PATIENT_RECORDS[patient_code]

    # Determine if the employee is authorized
    role_allowed = employee_role.lower() in ALLOWED_ROLES
    staff_assigned = employee_id in patient_record.get("assigned_staff", set())

    if not (role_allowed or staff_assigned):
        # Do not reveal whether the patient exists to avoid enumeration attacks
        raise PermissionError("Insufficient permissions to access this patient's data")

    # Return a copy to prevent accidental mutation of the internal database
    return dict(patient_record["medical_data"])