# -*- coding: utf-8 -*-
"""
Patient record access control module.

This module defines a single public function, `get_patient_record`, which
enforces proper authorization before returning sensitive medical data.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample patient records store
# --------------------------------------------------------------------------- #

PATIENT_RECORDS = {
    "P001": {
        "patient_id": "P001",
        # IDs of staff assigned to this patient
        "assigned_staff": ["D100", "N200"],
        # Example medical data; in a real system this would be more complex
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Monitor blood pressure daily."
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["D101", "N201"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin"],
            "notes": "Check HbA1c every 3 months."
        },
    },
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_authorized(
    personnel_id: str,
    personnel_role: str,
    record: dict[str, any]
) -> bool:
    """
    Determine if a personnel member is authorized to view the given record.

    Rules:
        * Admins have full access.
        * Doctors and nurses can view records only if they are in the
          record's `assigned_staff` list.
    """
    # Normalize role to lowercase for comparison
    role = personnel_role.lower()

    if role == "admin":
        return True

    # For other roles, check assignment
    if personnel_id in record.get("assigned_staff", []):
        return True

    # No other roles are permitted
    return False


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def get_patient_record(
    personnel_id: str,
    personnel_role: str,
    patient_identifier: str
) -> dict[str, any]:
    """
    Retrieve the medical data for a patient if access is authorized.

    Parameters
    ----------
    personnel_id : str
        The ID of the healthcare staff attempting to access the record.
    personnel_role : str
        The role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_identifier : str
        The ID of the patient whose records are being requested.

    Returns
    -------
    dict
        The medical data associated with the patient record.

    Raises
    ------
    PermissionError
        If the personnel member is not authorized to access the requested record.
    KeyError
        If the patient_identifier does not exist in `PATIENT_RECORDS`.
    """
    # Lookup record; raise KeyError if missing
    try:
        record = PATIENT_RECORDS[patient_identifier]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_identifier}' not found.") from exc

    # Authorization check
    if not _is_authorized(personnel_id, personnel_role, record):
        raise PermissionError(
            f"Personnel '{personnel_id}' with role '{personnel_role}' "
            "is not authorized to access patient record."
        )

    # Return a copy to prevent accidental mutation
    return dict(record["medical_data"])


# --------------------------------------------------------------------------- #
# Example usage (would normally be in separate test or application code)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example: doctor accessing assigned patient
    try:
        data = get_patient_record("D100", "doctor", "P001")
        print("Access granted. Medical data:")
        print(data)
    except Exception as exc:
        print(f"Error: {exc}")

    # Example: nurse trying to access unassigned patient
    try:
        data = get_patient_record("N201", "nurse", "P001")
    except Exception as exc:
        print(f"Error: {exc}")