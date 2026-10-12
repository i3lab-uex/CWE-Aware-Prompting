# -*- coding: utf-8 -*-
"""
Module providing secure access to patient records.

The implementation follows the principle of least privilege and ensures that
only authorized staff members can retrieve medical data.  The function raises
`PermissionError` if the requesting user does not have sufficient rights.
"""

from __future__ import annotations

# Sample patient records database.  In a real system this would be
# replaced by a secure persistence layer (e.g., encrypted database).
PATIENT_RECORDS: dict[str, dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": {"doctor_a", "nurse_b"},
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
            "notes": "Monitor blood pressure daily.",
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": {"doctor_c", "nurse_d"},
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin"],
            "notes": "Schedule HbA1c test in 3 months.",
        },
    },
}

def view_patient_record(
    staff_id: str,
    staff_role: str,
    patient_record_id: str
) -> dict:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Unique identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_record_id : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data dictionary.

    Raises
    ------
    KeyError
        If the patient record does not exist.
    PermissionError
        If the staff member is not authorized to view the record.
    """
    # Fetch the patient record
    try:
        record = PATIENT_RECORDS[patient_record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_record_id}' not found.") from exc

    # Authorization logic
    # 1. Admins can view any record.
    # 2. Doctors or nurses must be explicitly assigned to the patient.
    authorized = False
    if staff_role.lower() == "admin":
        authorized = True
    elif staff_id in record.get("assigned_staff", set()):
        # Assuming that doctors and nurses listed in assigned_staff are allowed
        authorized = True

    if not authorized:
        raise PermissionError(
            f"Staff '{staff_id}' with role '{staff_role}' "
            "does not have permission to view this patient record."
        )

    # Return only the medical data, not the entire record
    return record["medical_data"]

# Example usage (for demonstration purposes only):
if __name__ == "__main__":
    try:
        data = view_patient_record("doctor_a", "doctor", "patient_001")
        print("Medical Data:", data)
    except Exception as e:
        print(f"Error: {e}")