#!/usr/bin/env python3
"""
Module: patient_access

Provides a secure function for healthcare staff to review patient medical data.
"""

from typing import Dict, List, Any

# Example patient records (in a real system this would be loaded from a secure database)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_a1", "staff_b2"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["staff_c3"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Allowed staff roles and their permissions
ALLOWED_ROLES = {"doctor", "nurse", "admin"}


def review_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Return the medical data for a given patient if the staff member is authorized.

    Parameters
    ----------
    staff_id : str
        The ID of the healthcare personnel attempting to access the record.
    staff_role : str
        The role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        The ID of the patient whose records are being sought.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the patient's data.
    KeyError
        If the patient_id does not exist in PATIENT_RECORDS.
    ValueError
        If staff_role is invalid.
    """
    # Validate role
    if staff_role not in ALLOWED_ROLES:
        raise ValueError(f"Invalid staff role: {staff_role}")

    # Retrieve patient record
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:
        raise KeyError(f"Patient ID {patient_id} not found.") from exc

    # Authorization logic:
    # 1. Admins have blanket access.
    # 2. Non-admin staff can only view records if they are listed in assigned_staff.
    is_admin = staff_role == "admin"
    has_assignment = staff_id in record.get("assigned_staff", [])

    if not (is_admin or has_assignment):
        raise PermissionError(
            f"Staff '{staff_id}' with role '{staff_role}' is not authorized to access patient {patient_id}."
        )

    # Return a copy to prevent accidental modifications
    return dict(record.get("medical_data", {}))


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        data = review_patient_data("staff_a1", "nurse", "patient_001")
        print(f"Medical data retrieved: {data}")
    except Exception as e:
        print(f"Access failed: {e}")