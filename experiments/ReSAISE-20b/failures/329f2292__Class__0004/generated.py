#!/usr/bin/env python3
"""
Healthcare patient data review module.

The function `review_patient_data` enforces strict access control:
* A staff member may only view a patient's medical data if they are
  explicitly listed in the patient's `assigned_staff` list, or if
  their role is 'admin'.
* The check is case‑insensitive for roles.
* Unauthorized attempts raise a `PermissionError`.

CWE-863 (Incorrect Authorization) is mitigated by performing the
authorization check before any data retrieval and by not leaking
information about which part of the check failed.
"""

from __future__ import annotations

# Sample patient records dictionary
PATIENT_RECORDS = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

def review_patient_data(staff_id: str, staff_role: str, patient_id: str) -> dict:
    """
    Return the medical data for a given patient if the staff member is authorized.

    Parameters
    ----------
    staff_id : str
        The identifier of the healthcare personnel requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier of the patient whose data is being requested.

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
    """
    # Validate input types
    if not isinstance(staff_id, str) or not isinstance(staff_role, str) or not isinstance(patient_id, str):
        raise TypeError("All arguments must be strings.")

    # Retrieve patient record
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:
        # Do not reveal whether the patient exists to prevent enumeration
        raise PermissionError("Unauthorized access.") from exc

    # Authorization check: admin role or staff listed in assigned_staff
    authorized = False
    if staff_role.lower() == "admin":
        authorized = True
    elif staff_id in record.get("assigned_staff", []):
        authorized = True

    if not authorized:
        raise PermissionError("Unauthorized access.")

    # Return a copy to prevent accidental modification
    return dict(record["medical_data"])