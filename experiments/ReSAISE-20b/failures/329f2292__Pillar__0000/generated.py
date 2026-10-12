# -*- coding: utf-8 -*-
"""
Module: patient_access

Provides a secure way for healthcare staff to review patient medical data.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data (in a real system this would be fetched from a database)
# --------------------------------------------------------------------------- #
PATIENT_RECORDS: dict[str, dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_a", "staff_b"],  # staff IDs allowed to view
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Patient advised to reduce sodium intake."
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["staff_c"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin"],
            "notes": "Check HbA1c in 3 months."
        },
    },
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #
def review_patient_data(staff_id: str, staff_role: str, patient_id: str) -> dict:
    """
    Return the medical data for a given patient if the staff member has
    sufficient privileges and is assigned to the patient.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare personnel requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient_id is not found in PATIENT_RECORDS.
    """
    # Ensure patient exists
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_id}' not found.") from exc

    # Define allowed roles
    ALLOWED_ROLES = {"doctor", "nurse", "admin"}

    # Basic role validation
    if staff_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{staff_role}' is not authorized to view patient records."
        )

    # Role-based privilege: only doctors, nurses, and admins may access
    # Additional check: staff must be assigned to the patient unless role is admin
    if staff_role.lower() != "admin":
        if staff_id not in record["assigned_staff"]:
            raise PermissionError(
                f"Staff ID '{staff_id}' is not assigned to patient '{patient_id}'."
            )

    # All checks passed; return medical data
    return record["medical_data"]


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        data = review_patient_data("staff_a", "doctor", "patient_001")
        print("Medical data:", data)
    except PermissionError as e:
        print(f"Access denied: {e}")