# -*- coding: utf-8 -*-
"""
Medical record retrieval module.

This module implements the `retrieve_patient_data` function, which
enforces proper access control for healthcare professionals.
"""

from copy import deepcopy
from typing import Dict, Any

# Example patient records database (in practice this would be a secure datastore)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Diabetes"],
            "medications": ["Lisinopril", "Metformin"],
        },
    },
    # ... more patient records
}

# Roles that are allowed to view medical data
ALLOWED_ROLES = {"doctor", "nurse"}

def retrieve_patient_data(
    employee_id: str,
    employee_role: str,
    patient_code: str
) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record for an authorized employee.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the requesting healthcare professional.
    employee_role : str
        Role of the employee (e.g., 'doctor', 'nurse', 'admin').
    patient_code : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        A deep copy of the patient's medical data.

    Raises
    ------
    PermissionError
        If the employee is not authorized to view the record.
    KeyError
        If the patient_code does not exist in PATIENT_RECORDS.
    """
    # Ensure the requested patient exists
    if patient_code not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_code}' does not exist.")

    patient_record = PATIENT_RECORDS[patient_code]

    # Basic role check
    if employee_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{employee_role}' is not permitted to access medical records."
        )

    # Staff assignment check
    if employee_id not in patient_record.get("assigned_staff", []):
        raise PermissionError(
            f"Employee '{employee_id}' is not assigned to patient '{patient_code}'."
        )

    # Return a defensive copy of the medical data
    return deepcopy(patient_record.get("medical_data", {}))

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         data = retrieve_patient_data("doc123", "doctor", "patient_001")
#         print(data)
#     except PermissionError as e:
#         print(f"Access denied: {e}")