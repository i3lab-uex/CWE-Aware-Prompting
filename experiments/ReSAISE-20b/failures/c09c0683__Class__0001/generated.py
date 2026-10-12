# -*- coding: utf-8 -*-
"""
Secure patient data retrieval module.

This module defines a single public function, `retrieve_patient_data`, that
enforces strict authorization checks before exposing sensitive medical records.
The implementation follows the principles of least privilege and mitigates
CWE‑863 (Incorrect Authorization) by validating both the employee's role
and their explicit assignment to the requested patient.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data (in a real system this would be stored in a secure database)
# --------------------------------------------------------------------------- #

PATIENT_RECORDS = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["E123", "E456"],  # employee IDs with access
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": "Hypertension",
            "treatment_plan": ["Medication A", "Lifestyle changes"],
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["E789"],
        "medical_data": {
            "name": "Jane Smith",
            "age": 30,
            "diagnosis": "Asthma",
            "treatment_plan": ["Inhaler", "Allergy testing"],
        },
    },
}

# --------------------------------------------------------------------------- #
# Role-based permissions
# --------------------------------------------------------------------------- #

# Roles that are allowed to view any assigned patient's medical data.
ALLOWED_ROLES = {"doctor", "nurse"}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def retrieve_patient_data(
    employee_id: str,
    employee_role: str,
    patient_code: str,
) -> dict:
    """
    Retrieve a patient's medical data after verifying that the requesting
    employee has the appropriate role and is explicitly assigned to the patient.

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
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the employee does not have permission to view the patient's data.
    KeyError
        If the patient_code is not found in PATIENT_RECORDS.

    Notes
    -----
    The function performs a *two‑factor* authorization check:
        1. Role verification – only allowed roles may proceed.
        2. Assignment verification – the employee must be listed in
           `assigned_staff` for that patient.

    This approach protects against CWE‑863 by ensuring that no single
    condition suffices for access.
    """

    # 1. Validate patient existence
    if patient_code not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_code}' does not exist.")

    patient_record = PATIENT_RECORDS[patient_code]

    # 2. Role check
    if employee_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{employee_role}' is not authorized to access patient data."
        )

    # 3. Assignment check
    if employee_id not in patient_record["assigned_staff"]:
        raise PermissionError(
            f"Employee '{employee_id}' is not assigned to patient '{patient_code}'."
        )

    # 4. All checks passed – return a copy to prevent accidental mutation
    return patient_record["medical_data"].copy()


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove for production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        data = retrieve_patient_data("E123", "doctor", "P001")
        print("Medical Data Retrieved:")
        for k, v in data.items():
            print(f"  {k}: {v}")
    except PermissionError as pe:
        print(f"Access denied: {pe}")
    except KeyError as ke:
        print(f"Lookup error: {ke}")