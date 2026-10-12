# -*- coding: utf-8 -*-
"""
Utility module for accessing patient medical records with role‑based access control.
"""

from __future__ import annotations

import re
from typing import Dict, List, Any

# Example patient records. In a real system this would be fetched from a secure database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_a", "nurse_b"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_c"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Allowed roles that can bypass assignment checks
ADMIN_ROLES = {"admin", "superuser"}


def _validate_identifier(identifier: str) -> None:
    """
    Validate that an identifier is a non‑empty alphanumeric string.
    Raises ValueError if validation fails.
    """
    if not isinstance(identifier, str) or not identifier:
        raise ValueError("Identifier must be a non‑empty string.")
    if not re.match(r"^[A-Za-z0-9_\-]+$", identifier):
        raise ValueError("Identifier contains invalid characters.")


def fetch_patient_info(staff_identifier: str, staff_role: str, patient_ref: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a patient if the staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        ID of the healthcare personnel requesting access.
    staff_role : str
        Role of the requester (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        ID of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient reference is unknown.
    ValueError
        If any argument fails validation.
    """
    # Input validation
    _validate_identifier(staff_identifier)
    _validate_identifier(staff_role)
    _validate_identifier(patient_ref)

    # Retrieve patient record
    try:
        record = PATIENT_RECORDS[patient_ref]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_ref}' not found.") from exc

    # Authorization logic
    if staff_role.lower() in ADMIN_ROLES:
        # Admins can access any record
        authorized = True
    else:
        # Non‑admin staff must be explicitly assigned to the patient
        authorized = staff_identifier in record.get("assigned_staff", [])

    if not authorized:
        raise PermissionError(
            f"Unauthorized access: staff '{staff_identifier}' "
            f"with role '{staff_role}' cannot view patient '{patient_ref}'."
        )

    # Return a copy to prevent accidental mutation
    return dict(record["medical_data"])


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         data = fetch_patient_info("doc_a", "doctor", "patient_001")
#         print(data)
#     except Exception as e:
#         print(e)