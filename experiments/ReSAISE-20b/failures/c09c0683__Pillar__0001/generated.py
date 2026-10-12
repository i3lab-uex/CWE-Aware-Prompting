# -*- coding: utf-8 -*-
"""
Secure patient record retrieval module.

This module implements a single function `retrieve_patient_data` that
ensures only authorized healthcare workers can access a patient's medical data.
It follows best practices for access control to mitigate CWE‑284
(Improper Access Control) by:
- Verifying the employee's role.
- Checking that the employee is listed in the patient's assigned staff.
- Raising a clear PermissionError for any unauthorized attempts.

Author: OpenAI
"""

from typing import Dict, Any

# Example patient records database (would normally be a secure DB or encrypted store)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["emp_d1", "emp_n5"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["emp_d2"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Roles that are permitted to view medical data
ALLOWED_ROLES = {"doctor", "nurse"}


def retrieve_patient_data(employee_id: str, employee_role: str, patient_code: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting employee is authorized.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the healthcare professional.
    employee_role : str
        Role of the employee (e.g., 'doctor', 'nurse', 'admin').
    patient_code : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The medical data dictionary for the patient.

    Raises
    ------
    KeyError
        If the `patient_code` does not exist in PATIENT_RECORDS.
    PermissionError
        If the employee is not authorized to view the patient's record.
    """
    # Ensure patient exists
    if patient_code not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_code}' not found.")

    patient_record = PATIENT_RECORDS[patient_code]

    # Role-based access check
    if employee_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{employee_role}' is not authorized to access patient data."
        )

    # Staff assignment check
    if employee_id not in patient_record.get("assigned_staff", []):
        raise PermissionError(
            f"Employee '{employee_id}' is not assigned to patient '{patient_code}'."
        )

    # If all checks pass, return the medical data
    return patient_record["medical_data"]


# Example usage (would normally be in a separate test or application module)
if __name__ == "__main__":
    try:
        data = retrieve_patient_data("emp_d1", "doctor", "patient_001")
        print("Medical Data Retrieved:", data)
    except PermissionError as pe:
        print(f"Access denied: {pe}")
    except KeyError as ke:
        print(f"Lookup error: {ke}")