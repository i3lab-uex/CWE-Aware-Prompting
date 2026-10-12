#!/usr/bin/env python3
"""
Secure patient record retrieval module.

This module defines a single public function, `fetch_patient_record`, which
verifies that the requesting staff member is authorized to access a given
patient's medical record.  Authorization is based on both role‑based checks
and patient‑specific assignment.

The module deliberately follows the principle of least privilege and
avoids common CWE‑863 pitfalls by performing a single, comprehensive
authorization check before returning any sensitive data.
"""

from __future__ import annotations

from typing import Dict, List, Any


# --------------------------------------------------------------------------- #
# Example data store. In a real system this would be replaced by a secure
# database access layer with proper encryption at rest and in transit.
# --------------------------------------------------------------------------- #
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["dr_smith", "nurse_jane"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["lisinopril"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["dr_brown"],
        "medical_data": {
            "diagnosis": "Diabetes Type 2",
            "medications": ["metformin"],
        },
    },
}


# --------------------------------------------------------------------------- #
# Custom exception for unauthorized access attempts.
# --------------------------------------------------------------------------- #
class PermissionError(Exception):
    """Raised when a staff member is not authorized to access a patient record."""


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def fetch_patient_record(
    staff_identifier: str,
    staff_role: str,
    patient_ident: str,
) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record after performing an authorization check.

    Parameters
    ----------
    staff_identifier : str
        Unique identifier of the requesting healthcare professional.
    staff_role : str
        Role of the requester (e.g., 'doctor', 'nurse', 'admin', etc.).
    patient_ident : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the record.
    KeyError
        If the patient identifier does not exist in `PATIENT_RECORDS`.
    """
    # 1. Verify that the patient exists
    try:
        record = PATIENT_RECORDS[patient_ident]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_ident}' not found.") from exc

    # 2. Role-based authorization
    allowed_roles: List[str] = ["doctor", "nurse", "admin"]
    if staff_role.lower() not in allowed_roles:
        raise PermissionError(
            f"Role '{staff_role}' is not permitted to access patient records."
        )

    # 3. Patient-specific assignment check
    if staff_identifier not in record.get("assigned_staff", []):
        # Even admins must be assigned to the patient in this simplified model
        raise PermissionError(
            f"Staff '{staff_identifier}' is not assigned to patient '{patient_ident}'."
        )

    # 4. All checks passed; return the medical data
    return record["medical_data"]


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        data = fetch_patient_record("dr_smith", "doctor", "patient_001")
        print("Medical data retrieved:", data)
    except Exception as e:
        print(f"Access failed: {e}")