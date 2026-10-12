#!/usr/bin/env python3
"""
Medical record access module.

Author: OpenAI ChatGPT
Date: 2026-07-23

This module defines a secure function `view_patient_record` that enforces
strict authorization checks before exposing sensitive medical data.
The implementation follows the principle of least privilege and guards
against CWE‑863 (Incorrect Authorization).
"""

from __future__ import annotations

import json
from typing import Dict, List, Any


# --------------------------------------------------------------------------- #
# 1. Sample patient records data store
# --------------------------------------------------------------------------- #

PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient-001": {
        "patient_id": "patient-001",
        # The staff members (by ID) who are explicitly allowed to view this record
        "assigned_staff": ["staff-123", "staff-456"],
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Type II Diabetes"],
            "medications": [
                {"name": "Lisinopril", "dose_mg": 20},
                {"name": "Metformin", "dose_mg": 500}
            ],
        },
    },
    "patient-002": {
        "patient_id": "patient-002",
        "assigned_staff": ["staff-789"],
        "medical_data": {
            "name": "Jane Smith",
            "age": 30,
            "diagnosis": ["Asthma"],
            "medications": [
                {"name": "Albuterol", "dose_mg": 90}
            ],
        },
    },
}


# --------------------------------------------------------------------------- #
# 2. Helper functions
# --------------------------------------------------------------------------- #

def _is_staff_authorized(
    staff_id: str,
    staff_role: str,
    patient_record: Dict[str, Any],
) -> bool:
    """
    Determine if a staff member is allowed to view the given patient record.

    Authorization logic:
      * The staff must have a role that is permitted (doctor or nurse).
      * The staff ID must be in the record's `assigned_staff` list.

    Args:
        staff_id: Unique identifier of the requesting staff member.
        staff_role: Role string (e.g., 'doctor', 'nurse', 'admin').
        patient_record: The full patient record dictionary.

    Returns:
        True if authorized, False otherwise.
    """
    # Roles that are permitted to view records
    allowed_roles = {"doctor", "nurse"}

    # Role check (case‑insensitive to avoid subtle bypasses)
    if staff_role.lower() not in allowed_roles:
        return False

    # Membership check: ensure the ID is present in the assigned_staff list
    return staff_id in patient_record.get("assigned_staff", [])


# --------------------------------------------------------------------------- #
# 3. Main API function
# --------------------------------------------------------------------------- #

def view_patient_record(
    staff_id: str,
    staff_role: str,
    patient_record_id: str,
) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member
    is authorized.

    The function performs:
      1. Input validation (non‑empty strings)
      2. Record existence check
      3. Strict authorization check

    Args:
        staff_id: Unique identifier of the healthcare professional.
        staff_role: Role of the staff member ('doctor', 'nurse', etc.).
        patient_record_id: Identifier for the patient record.

    Returns:
        The `medical_data` dictionary of the requested patient.

    Raises:
        KeyError: If the patient record does not exist.
        PermissionError: If the staff member is not authorized to view the record.
    """
    # 1. Basic input validation
    if not all(isinstance(x, str) and x.strip() for x in (staff_id, staff_role, patient_record_id)):
        raise ValueError("All arguments must be non‑empty strings.")

    # 2. Retrieve the patient record
    try:
        record = PATIENT_RECORDS[patient_record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_record_id}' not found.") from exc

    # 3. Authorization check
    if not _is_staff_authorized(staff_id, staff_role, record):
        raise PermissionError(
            f"Staff '{staff_id}' with role '{staff_role}' is not authorized to view record "
            f"'{patient_record_id}'."
        )

    # 4. Return a deep copy to prevent accidental mutation
    return json.loads(json.dumps(record["medical_data"]))


# --------------------------------------------------------------------------- #
# 4. Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Successful access
    try:
        data = view_patient_record("staff-123", "Doctor", "patient-001")
        print("Access granted. Medical data:")
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")

    # Unauthorized access
    try:
        data = view_patient_record("staff-999", "Nurse", "patient-001")
    except Exception as e:
        print(f"Error: {e}")