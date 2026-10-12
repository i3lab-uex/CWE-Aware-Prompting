# -*- coding: utf-8 -*-
"""
Health record access module.

The function `fetch_patient_record` implements an access control check
against a simple in‑memory patient record store.  It raises a
`PermissionError` (CWE-284) when the requesting staff member does not
have permission to read a given patient's medical data.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from typing import Dict, List, Any


# Example patient record store.
# In a real system this would be replaced by a secure database layer.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_a123", "nurse_b456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_c789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["metformin"]},
    },
}


def fetch_patient_record(
    staff_identifier: str,
    staff_role: str,
    patient_ident: str,
) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        The unique ID of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin',
        'receptionist').
    patient_ident : str
        The unique ID of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the record.
    KeyError
        If `patient_ident` does not exist in :data:`PATIENT_RECORDS`.
    """
    # Ensure the patient record exists.
    if patient_ident not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_ident}' does not exist.")

    patient_record = PATIENT_RECORDS[patient_ident]

    # Define roles that have blanket access.
    privileged_roles: List[str] = ["admin", "doctor"]

    # Access is granted if:
    # 1. The staff role is privileged (e.g., admin or doctor), OR
    # 2. The staff identifier is listed in the patient's assigned_staff.
    if (
        staff_role.lower() in privileged_roles
        or staff_identifier in patient_record.get("assigned_staff", [])
    ):
        return patient_record["medical_data"]

    # If none of the conditions are met, deny access.
    raise PermissionError(
        f"Unauthorized access attempt by staff '{staff_identifier}' "
        f"(role: {staff_role}) to patient record '{patient_ident}'."
    )


# Example usage (for demonstration; remove or guard with `if __name__ == "__main__":` in production)
if __name__ == "__main__":
    try:
        data = fetch_patient_record("doc_a123", "doctor", "patient_001")
        print("Medical Data:", data)
    except PermissionError as e:
        print(e)