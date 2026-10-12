# -*- coding: utf-8 -*-
"""
Patient record access module

This module defines a simple in‑memory data store and an access control
function that enforces the following rules:

* Only staff members listed in a patient's `assigned_staff` list can view
  that patient's medical data.
* Users with the role ``admin`` are allowed to view any record regardless
  of assignment.
* All other roles are denied access if the staff ID is not explicitly
  assigned to the patient.

The function raises :class:`PermissionError` for unauthorized access.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample patient records data store
# --------------------------------------------------------------------------- #

PATIENT_RECORDS = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_a", "staff_b"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril 10mg"],
            "last_visit": "2024-06-12",
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["staff_c"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin 500mg"],
            "last_visit": "2024-05-28",
        },
    },
    # Additional patient records can be added here.
}

# --------------------------------------------------------------------------- #
# Access control function
# --------------------------------------------------------------------------- #

def review_patient_data(staff_id: str, staff_role: str, patient_id: str) -> dict:
    """
    Return the medical data for a patient if the requesting staff member
    is authorized to view it.

    Parameters
    ----------
    staff_id : str
        Identifier of the staff member attempting to access the record.
    staff_role : str
        Role of the staff member. Accepted values are 'doctor', 'nurse',
        and 'admin'. The role comparison is case‑insensitive.
    patient_id : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data dictionary.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to access the requested record.
    KeyError
        If the patient_id does not exist in :data:`PATIENT_RECORDS`.
    """
    # Validate patient existence
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_id}' not found.") from exc

    # Normalise role for case‑insensitive comparison
    normalized_role = staff_role.strip().lower()

    # Admins bypass assignment checks
    if normalized_role == "admin":
        return record["medical_data"]

    # Non‑admin roles must be in the assigned_staff list
    if staff_id not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Staff member '{staff_id}' with role '{staff_role}' "
            "is not authorized to view this patient record."
        )

    # Authorized access
    return record["medical_data"]

# --------------------------------------------------------------------------- #
# Example usage (for testing purposes)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Authorized access
    try:
        data = review_patient_data("staff_a", "doctor", "patient_001")
        print("Medical data retrieved:", data)
    except Exception as e:
        print("Error:", e)

    # Unauthorized access
    try:
        data = review_patient_data("staff_x", "nurse", "patient_001")
    except Exception as e:
        print("Error:", e)