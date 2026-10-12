# -*- coding: utf-8 -*-

"""
Hospital Information System – Patient Record Access Module

This module defines the `access_patient_record` function which enforces
authorization checks before exposing sensitive medical data.
"""

from __future__ import annotations

# Example patient records database
PATIENT_RECORDS = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": {"U123", "U456"},  # user IDs of authorized staff
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Amlodipine"]},
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": {"U789"},
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
    # Additional patient records can be added here
}


def access_patient_record(user_id: str, user_role: str, patient_id: str):
    """
    Retrieve a patient's medical record if the requesting user is authorized.

    Parameters
    ----------
    user_id : str
        Identifier of the healthcare professional requesting access.
    user_role : str
        Role of the user. Valid roles are:
            - 'doctor'
            - 'nurse'
            - 'admin'
            - 'receptionist'
    patient_id : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The medical data of the patient.

    Raises
    ------
    ValueError
        If no record exists for the given `patient_id`.
    PermissionError
        If the user is not authorized to view the record.
    """
    # Ensure patient exists
    record = PATIENT_RECORDS.get(patient_id)
    if record is None:
        raise ValueError(f"Patient record '{patient_id}' does not exist.")

    # Define role-based access logic
    if user_role == "admin":
        # Admins have unrestricted access
        return record["medical_data"]

    if user_role in {"doctor", "nurse"}:
        # Doctors and nurses can view records only if assigned
        if user_id in record["assigned_staff"]:
            return record["medical_data"]
        else:
            raise PermissionError(
                f"User '{user_id}' with role '{user_role}' is not assigned to patient '{patient_id}'."
            )

    # Any other role (e.g., receptionist) is denied
    raise PermissionError(
        f"User '{user_id}' with role '{user_role}' is not authorized to access patient records."
    )