# -*- coding: utf-8 -*-
"""
Patient data access control module.

This module provides a single function `review_patient_data` that
enforces role‑based and assignment‑based access control on patient
records stored in the `PATIENT_RECORDS` dictionary.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample patient records – in a real system this would be fetched from a
# secure database or encrypted storage.
# --------------------------------------------------------------------------- #
PATIENT_RECORDS = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_a", "nurse_b"],
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Type II Diabetes"],
            "medications": ["Lisinopril", "Metformin"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_c"],
        "medical_data": {
            "name": "Jane Smith",
            "age": 30,
            "diagnosis": ["Asthma"],
            "medications": ["Albuterol"],
        },
    },
}

# --------------------------------------------------------------------------- #
# Access control implementation
# --------------------------------------------------------------------------- #
def review_patient_data(staff_id: str, staff_role: str, patient_id: str) -> dict:
    """
    Return the medical data for a patient if the requesting staff member
    is authorized to view it.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare personnel requesting access.
    staff_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier of the patient whose data is being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    KeyError
        If the patient_id is not present in PATIENT_RECORDS.
    PermissionError
        If the staff member does not have permission to view the record.
    """
    # 1. Validate patient existence
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_id}' not found.") from exc

    # 2. Authorization checks
    authorized = False

    # Admins can view any record
    if staff_role.lower() == "admin":
        authorized = True

    # Staff assigned to the patient can view their own record
    if staff_id in record.get("assigned_staff", []):
        authorized = True

    # Optional: doctors can view any record (policy decision)
    if staff_role.lower() == "doctor":
        authorized = True

    # 3. Enforce access control
    if not authorized:
        raise PermissionError(
            f"Unauthorized: staff_id '{staff_id}' with role '{staff_role}' "
            f"is not permitted to access patient '{patient_id}'."
        )

    # 4. Return a copy of medical data to avoid accidental mutation
    return record["medical_data"].copy()


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        data = review_patient_data("doctor_a", "doctor", "patient_001")
        print("Medical Data:", data)
    except Exception as e:
        print(f"Error: {e}")