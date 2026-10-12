# -*- coding: utf-8 -*-
"""
Patient data access module.

This module defines a single function, `review_patient_data`, which
enforces correct authorization before returning sensitive medical data.
The implementation follows the principles of secure coding and mitigates
the risk of CWE‑863 (Incorrect Authorization).
"""

from __future__ import annotations

# Example patient records database.
# In a real system this would be replaced by a secure data store.
PATIENT_RECORDS = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": {"doctor_123", "nurse_456"},
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
            "notes": "Patient to monitor blood pressure daily."
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": {"doctor_789"},
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin"],
            "notes": "Schedule follow-up in 3 months."
        },
    },
}


def review_patient_data(staff_id: str, staff_role: str, patient_id: str) -> dict:
    """
    Return the medical data for a given patient if and only if the staff member
    has proper authorization.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare personnel attempting to access the record.
    staff_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier of the patient whose records are being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient_id is unknown in the system.
    """

    # Validate input types to avoid type confusion attacks
    if not isinstance(staff_id, str):
        raise TypeError("staff_id must be a string")
    if not isinstance(staff_role, str):
        raise TypeError("staff_role must be a string")
    if not isinstance(patient_id, str):
        raise TypeError("patient_id must be a string")

    # Retrieve patient record
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:
        # For security, we do not reveal whether the patient exists
        raise KeyError("Patient record not found") from exc

    # Authorization logic
    # 1. Admins can access any record.
    # 2. Staff must be listed in the assigned_staff set for the patient.
    # The comparison is performed using a set membership check to avoid
    # pitfalls such as substring matching or case sensitivity issues.
    authorized = False

    if staff_role.lower() == "admin":
        authorized = True
    else:
        # Use a set for O(1) membership checks; assigned_staff is expected to be
        # stored as a set or convertible to one.
        assigned = record.get("assigned_staff", set())
        if isinstance(assigned, (list, tuple)):
            assigned = set(assigned)
        authorized = staff_id in assigned

    if not authorized:
        raise PermissionError("Unauthorized access to patient data")

    # Return a copy of the medical_data to prevent accidental mutation
    return dict(record["medical_data"])


# Example usage (commented out to avoid accidental execution)
# try:
#     data = review_patient_data("doctor_123", "Doctor", "patient_001")
#     print(data)
# except PermissionError as e:
#     print(e)