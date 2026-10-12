# -*- coding: utf-8 -*-
"""
Medical record access module.

The function `fetch_patient_info` implements an access control policy
that allows a healthcare staff member to retrieve a patient's medical data
only if the staff is authorized.  Unauthorized attempts raise a
`PermissionError`.

CWE-284: Improper Access Control is mitigated by checking both the
staff's identifier and role against the patient record before exposing any
sensitive data.
"""

from typing import Dict, Any, List

# Example patient records structure.  In a real system this would come from
# a secure database or an external service.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_alice", "nurse_bob"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Monitor blood pressure daily."
        },
    },
    # Additional patient records would be added here.
}


def fetch_patient_info(staff_identifier: str,
                       staff_role: str,
                       patient_ref: str) -> Dict[str, Any]:
    """
    Retrieve medical data for a given patient if the requesting staff member
    has proper authorization.

    Parameters:
        staff_identifier (str): Unique ID of the healthcare personnel.
        staff_role (str): Role of the staff member ('doctor', 'nurse', 'admin',
                          etc.).
        patient_ref (str): Patient ID whose record is requested.

    Returns:
        dict: The patient's medical data.

    Raises:
        PermissionError: If the staff member is not authorized to view
                         the requested record.
        KeyError: If the patient_ref does not exist in PATIENT_RECORDS.
    """
    # Validate that the patient exists
    try:
        record = PATIENT_RECORDS[patient_ref]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_ref}' not found.") from exc

    # Authorization logic:
    # - Admins can view any record.
    # - Doctors and nurses can view only if they are listed in assigned_staff.
    authorized = False

    if staff_role.lower() == "admin":
        authorized = True
    else:
        # Ensure the assigned_staff list exists and is a list of strings.
        staff_list: List[str] = record.get("assigned_staff", [])
        if not isinstance(staff_list, list):
            staff_list = []

        # Check membership in a case-insensitive manner.
        authorized = any(
            staff_identifier.lower() == member.lower()
            for member in staff_list
        )

    if not authorized:
        raise PermissionError(
            f"Unauthorized access attempt by staff '{staff_identifier}' "
            f"(role: {staff_role}) to patient '{patient_ref}'."
        )

    # Return a copy of the medical data to avoid accidental mutation.
    return dict(record.get("medical_data", {}))