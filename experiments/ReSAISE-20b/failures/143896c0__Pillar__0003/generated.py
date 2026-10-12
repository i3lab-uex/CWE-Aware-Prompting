# -*- coding: utf-8 -*-
"""
Medical Record Access Module

This module provides a single public function `view_patient_record` that
returns medical data for a patient after performing an authorization check.
The implementation follows the principle of least privilege and is designed
to mitigate CWE-284: Improper Access Control.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
#  Mock patient records database
# --------------------------------------------------------------------------- #
PATIENT_RECORDS = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": {"S123", "S456"},  # staff IDs allowed to view
        "medical_data": {
            "name": "Alice Smith",
            "age": 29,
            "diagnosis": ["Hypertension"],
            "treatment_plan": ["Low-sodium diet", "Regular exercise"]
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": {"S789"},  # only one staff member allowed
        "medical_data": {
            "name": "Bob Johnson",
            "age": 45,
            "diagnosis": ["Type 2 Diabetes"],
            "treatment_plan": ["Metformin", "Blood sugar monitoring"]
        },
    },
}

# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #

def view_patient_record(staff_id: str, staff_role: str, patient_record_id: str) -> dict:
    """
    Retrieve a patient's medical record after verifying that the requesting
    staff member is authorized to view it.

    Parameters
    ----------
    staff_id : str
        Unique identifier of the healthcare professional making the request.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_record_id : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data if access is authorized.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient_record_id is not found in PATIENT_RECORDS.
    """
    # 1. Validate existence of the patient record
    if patient_record_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_record_id}' does not exist.")

    patient = PATIENT_RECORDS[patient_record_id]

    # 2. Authorization: Only staff listed in `assigned_staff` may view
    if staff_id not in patient["assigned_staff"]:
        # Log the unauthorized attempt (placeholder for real logging)
        _log_unauthorized_access(staff_id, patient_record_id)
        raise PermissionError(
            f"Staff '{staff_id}' is not authorized to view record '{patient_record_id}'."
        )

    # 3. Return a copy of the medical data to prevent accidental mutation
    return patient["medical_data"].copy()


# --------------------------------------------------------------------------- #
#  Internal helper functions
# --------------------------------------------------------------------------- #

def _log_unauthorized_access(staff_id: str, patient_record_id: str) -> None:
    """
    Log an unauthorized access attempt. In a real system, this would
    interface with a secure audit logging mechanism.

    Parameters
    ----------
    staff_id : str
        Identifier of the staff member who attempted access.
    patient_record_id : str
        The patient record that was attempted to be accessed.
    """
    # For demonstration purposes, we simply print. Replace with real logging.
    print(f"[SECURITY] Unauthorized access attempt: staff_id={staff_id}, "
          f"patient_record_id={patient_record_id}")


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Authorized access
    try:
        data = view_patient_record("S123", "doctor", "P001")
        print("Medical Data:", data)
    except Exception as e:
        print(e)

    # Unauthorized access
    try:
        data = view_patient_record("S999", "nurse", "P001")
    except Exception as e:
        print(e)