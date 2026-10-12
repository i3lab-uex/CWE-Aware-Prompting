#!/usr/bin/env python3
"""
Patient data access module.

This module implements a secure function to retrieve patient records while ensuring
that only authorized healthcare workers can access sensitive medical data.
"""

from __future__ import annotations

import typing as _t

# --------------------------------------------------------------------------- #
# Sample patient records database
# --------------------------------------------------------------------------- #

PATIENT_RECORDS: dict[str, dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["worker_a", "worker_b"],  # staff IDs who can view this record
        "medical_data": {
            "diagnosis": "Hypertension",
            "treatment_plan": ["Medication A", "Lifestyle changes"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["worker_c"],
        "medical_data": {
            "diagnosis": "Diabetes",
            "treatment_plan": ["Insulin", "Diet plan"],
        },
    },
    # ... more records ...
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def get_patient_data(worker_id: str, worker_role: str, record_id: str) -> dict:
    """
    Retrieve a patient's medical data after performing an authorization check.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the healthcare professional requesting the record.
    worker_role : str
        Role of the worker (e.g., 'doctor', 'nurse', 'admin').
    record_id : str
        Identifier of the patient whose record is being retrieved.

    Returns
    -------
    dict
        The medical data portion of the patient's record.

    Raises
    ------
    KeyError
        If the requested patient record does not exist.
    PermissionError
        If the worker is not authorized to view the requested record.
    """
    # Validate that the record exists
    try:
        patient_record = PATIENT_RECORDS[record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{record_id}' not found.") from exc

    # Authorization logic
    authorized = False

    # 1. Admins can access any record
    if worker_role.lower() == "admin":
        authorized = True

    # 2. Doctors can access any record (or restrict further if needed)
    elif worker_role.lower() == "doctor":
        authorized = True

    # 3. Other roles can only access records where they are explicitly assigned
    else:
        if worker_id in patient_record.get("assigned_staff", []):
            authorized = True

    if not authorized:
        raise PermissionError(
            f"Worker '{worker_id}' with role '{worker_role}' "
            "is not authorized to access record '{}'.".format(record_id)
        )

    # Return only the medical data portion
    return patient_record.get("medical_data", {})

# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example calls demonstrating authorization
    try:
        data = get_patient_data("worker_a", "nurse", "patient_001")
        print("Access granted. Medical data:", data)
    except Exception as e:
        print(e)

    try:
        data = get_patient_data("worker_x", "nurse", "patient_001")
        print("Access granted. Medical data:", data)
    except Exception as e:
        print(e)