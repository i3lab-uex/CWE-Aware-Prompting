# -*- coding: utf-8 -*-
"""
Secure patient data access module.

This module defines a function `get_patient_data` that allows
healthcare staff to retrieve patient medical records while enforcing
role‑based access control.  Unauthorized requests raise a
`PermissionError`.

Author: ChatGPT
"""

from typing import Dict, List, Any

# --------------------------------------------------------------------------- #
# Example patient records. In a real application this data would be fetched
# from a secure database rather than stored in memory.
# --------------------------------------------------------------------------- #
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        # Staff IDs who are explicitly allowed to view this record
        "assigned_staff": ["S123", "S456"],
        "medical_data": {
            "name": "John Doe",
            "age": 42,
            "diagnosis": ["Hypertension", "Type II Diabetes"],
            "medications": ["Lisinopril 10mg", "Metformin 500mg"],
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["S789"],
        "medical_data": {
            "name": "Jane Smith",
            "age": 35,
            "diagnosis": ["Asthma"],
            "medications": ["Albuterol inhaler"],
        },
    },
}

# --------------------------------------------------------------------------- #
# Role hierarchy: Admin has full access; doctors and nurses may access
# records only if they are listed in `assigned_staff`. Other roles are
# denied by default.
# --------------------------------------------------------------------------- #
ALLOWED_ROLES_WITH_FULL_ACCESS = {"admin"}
ALLOWED_ROLES_RESTRICTED_ACCESS = {"doctor", "nurse"}

def get_patient_data(staff_num: str, role: str, patient_ref: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a specific patient if the requesting
    staff member is authorized.

    Parameters
    ----------
    staff_num : str
        The unique identifier of the healthcare professional.
    role : str
        The staff member's role (e.g., 'doctor', 'nurse', 'admin',
        'receptionist', etc.).
    patient_ref : str
        The identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If `patient_ref` is not found in :data:`PATIENT_RECORDS`.
    """
    # Normalize role for comparison
    normalized_role = role.strip().lower()

    # Fetch the patient record; raise KeyError if not found
    try:
        record = PATIENT_RECORDS[patient_ref]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_ref}' does not exist.") from exc

    # Determine authorization
    authorized = False

    if normalized_role in ALLOWED_ROLES_WITH_FULL_ACCESS:
        # Admins can view any record
        authorized = True
    elif normalized_role in ALLOWED_ROLES_RESTRICTED_ACCESS:
        # Doctors and nurses must be explicitly assigned
        authorized = staff_num in record.get("assigned_staff", [])
    else:
        # Other roles are not permitted to view medical data
        authorized = False

    if not authorized:
        raise PermissionError(
            f"Staff '{staff_num}' with role '{role}' is not authorized "
            f"to access patient record '{patient_ref}'."
        )

    # Return a copy to prevent accidental mutation of the original data
    return dict(record["medical_data"])