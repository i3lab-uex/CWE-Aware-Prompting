# -*- coding: utf-8 -*-
"""
Secure patient record retrieval module.

This module implements the `retrieve_patient_data` function that enforces
proper access control based on employee role and patient assignment.
"""

from __future__ import annotations

# ----------------------------------------------------------------------
# Sample data store (would normally be a secure database)
# ----------------------------------------------------------------------
PATIENT_RECORDS: dict[str, dict] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": {"doctor_123", "nurse_456"},
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": "Hypertension",
            "treatment_plan": ["Medication A", "Lifestyle changes"],
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": {"doctor_789"},
        "medical_data": {
            "name": "Jane Smith",
            "age": 30,
            "diagnosis": "Asthma",
            "treatment_plan": ["Inhaler", "Avoid allergens"],
        },
    },
}

# ----------------------------------------------------------------------
# Role-based access control policy
# ----------------------------------------------------------------------
# Allowed roles that can request patient data
ALLOWED_ROLES = {"doctor", "nurse"}

# ----------------------------------------------------------------------
def retrieve_patient_data(
    employee_id: str,
    employee_role: str,
    patient_code: str,
) -> dict:
    """
    Retrieve a patient's medical record after performing access control checks.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the requesting healthcare professional.
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
        If the employee is not authorized to view the record.
    KeyError
        If the patient_code does not exist in PATIENT_RECORDS.
    """
    # --- 1. Validate role ------------------------------------------------
    if employee_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{employee_role}' is not permitted to access patient records."
        )

    # --- 2. Retrieve patient record ---------------------------------------
    try:
        patient_record = PATIENT_RECORDS[patient_code]
    except KeyError as exc:
        raise KeyError(f"Patient code '{patient_code}' not found.") from exc

    # --- 3. Verify staff assignment --------------------------------------
    if employee_id not in patient_record.get("assigned_staff", set()):
        raise PermissionError(
            f"Employee '{employee_id}' is not assigned to patient '{patient_code}'."
        )

    # --- 4. Return the medical data --------------------------------------
    return patient_record["medical_data"]

# ----------------------------------------------------------------------
# Example usage (for testing purposes)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        data = retrieve_patient_data("doctor_123", "doctor", "P001")
        print("Retrieved data:", data)
    except PermissionError as pe:
        print(f"Access denied: {pe}")
    except KeyError as ke:
        print(f"Lookup error: {ke}")