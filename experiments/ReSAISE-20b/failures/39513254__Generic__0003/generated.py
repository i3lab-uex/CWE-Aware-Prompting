# -*- coding: utf-8 -*-
"""
Hospital Information System – Patient Record Access Module

This module defines the `access_patient_record` function which enforces
role‑based access control when retrieving a patient’s medical data.
"""

from __future__ import annotations

# Example in‑memory database of patient records
PATIENT_RECORDS = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": {"doctor:U123", "nurse:N456"},
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Diabetes"],
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": {"doctor:U789"},
        "medical_data": {
            "name": "Jane Smith",
            "age": 30,
            "diagnosis": ["Asthma"],
        },
    },
}


def _normalize_user_identity(user_role: str, user_id: str) -> str:
    """
    Convert a user role and ID into the format used in `assigned_staff`.

    Parameters
    ----------
    user_role : str
        Role of the user (e.g., 'doctor', 'nurse').
    user_id : str
        Unique identifier of the user.

    Returns
    -------
    str
        Normalized identity string, e.g. 'doctor:U123'.
    """
    return f"{user_role.lower()}:{user_id}"


def access_patient_record(user_id: str, user_role: str, patient_id: str):
    """
    Retrieve a patient's medical data after performing authorization checks.

    Parameters
    ----------
    user_id : str
        The ID of the healthcare professional attempting access.
    user_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin', or 'receptionist').
    patient_id : str
        The ID of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data if the user is authorized.

    Raises
    ------
    ValueError
        If the patient record does not exist.
    PermissionError
        If the user is not authorized to view the patient's data.
    TypeError
        If any argument is not a string.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (user_id, user_role, patient_id)):
        raise TypeError("All arguments must be strings.")

    # Retrieve the patient's record
    patient_record = PATIENT_RECORDS.get(patient_id)
    if patient_record is None:
        raise ValueError(f"Patient record with ID '{patient_id}' does not exist.")

    # Authorization logic
    role = user_role.lower()
    if role == "admin":
        # Admins have full read access
        return patient_record["medical_data"]

    if role in {"doctor", "nurse"}:
        # Doctors and nurses can only access records where they are assigned
        identity = _normalize_user_identity(role, user_id)
        if identity in patient_record["assigned_staff"]:
            return patient_record["medical_data"]

    # All other roles (e.g., receptionist) are denied access
    raise PermissionError(
        f"User '{user_id}' with role '{user_role}' is not authorized to access "
        f"patient record '{patient_id}'."
    )


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         data = access_patient_record("U123", "doctor", "P001")
#         print(data)
#     except Exception as e:
#         print(f"Access denied: {e}")