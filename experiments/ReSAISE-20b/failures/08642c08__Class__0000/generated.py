# -*- coding: utf-8 -*-
"""
Authorisation helper for accessing patient records.

The function `fetch_patient_info` enforces strict access control:
  * The staff member must be present in the patient's `assigned_staff` list
    **or** have an administrative role.
  * No implicit or partial matches are allowed (CWE‑863).
"""

from __future__ import annotations

# Example patient records database.
# In a real system this would be replaced by a secure persistent store.
PATIENT_RECORDS = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["D123", "N456"],
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": "Hypertension",
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["D789"],
        "medical_data": {
            "name": "Jane Smith",
            "age": 30,
            "diagnosis": "Diabetes",
        },
    },
}


def fetch_patient_info(staff_identifier: str, staff_role: str, patient_ref: str):
    """
    Retrieve a patient's medical data if the requesting staff member is authorised.

    Parameters
    ----------
    staff_identifier : str
        The unique identifier of the healthcare personnel requesting access.
    staff_role : str
        The role of the requester (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        The unique identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    KeyError
        If the patient_ref does not exist in PATIENT_RECORDS.
    PermissionError
        If the staff member is not authorised to view the record.
    """

    # 1. Validate that the patient exists
    if patient_ref not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_ref}' not found.")

    patient_record = PATIENT_RECORDS[patient_ref]

    # 2. Authorisation logic
    is_admin = staff_role.lower() == "admin"
    # Explicit membership test – no substring matching.
    is_assigned = staff_identifier in patient_record["assigned_staff"]

    if not (is_admin or is_assigned):
        raise PermissionError(
            f"Unauthorized access attempt by staff '{staff_identifier}' "
            f"(role: {staff_role}) to patient '{patient_ref}'."
        )

    # 3. Return the medical data
    return patient_record["medical_data"]


# Example usage (commented out to avoid accidental execution)
# try:
#     data = fetch_patient_info("D123", "doctor", "P001")
#     print(data)
# except Exception as e:
#     print(e)