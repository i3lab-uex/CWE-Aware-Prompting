# -*- coding: utf-8 -*-
"""
Medical record access module.

Provides a secure function to retrieve patient medical data
while enforcing strict role‑based and assignment checks.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data structure.  In a real system this would be backed by a database.
# --------------------------------------------------------------------------- #
PATIENT_RECORDS: dict[str, dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        # List of staff IDs that are allowed to view this record.
        "assigned_staff": ["staff_100", "staff_101"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["staff_102"],
        "medical_data": {
            "diagnosis": "Diabetes Type 2",
            "medications": ["Metformin"],
        },
    },
}


def get_patient_record(
    personnel_id: str,
    personnel_role: str,
    patient_identifier: str,
) -> dict:
    """
    Retrieve the medical data for a given patient if access is authorized.

    Parameters
    ----------
    personnel_id : str
        Identifier of the healthcare staff attempting access.
    personnel_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_identifier : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The medical data for the specified patient.

    Raises
    ------
    KeyError
        If the patient identifier does not exist in ``PATIENT_RECORDS``.
    PermissionError
        If the user is not authorized to view the patient's record.

    Notes
    -----
    * Admin users are granted unrestricted access.
    * Other roles must be explicitly listed in the patient's
      ``assigned_staff`` list.
    """
    # 1. Verify patient exists
    try:
        record = PATIENT_RECORDS[patient_identifier]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_identifier}' not found.") from exc

    # 2. Access control checks
    if personnel_role.lower() == "admin":
        # Admins bypass all checks.
        return record["medical_data"]

    # Non‑admin roles must be explicitly assigned to the patient.
    if personnel_id not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Personnel ID '{personnel_id}' with role '{personnel_role}' "
            "is not authorized to access this patient record."
        )

    # 3. Return the sensitive data
    return record["medical_data"]


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        data = get_patient_record("staff_100", "doctor", "patient_001")
        print("Medical Data:", data)
    except Exception as e:
        print(e)