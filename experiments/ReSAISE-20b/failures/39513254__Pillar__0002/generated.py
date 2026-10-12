#!/usr/bin/env python3
"""
Hospital Information System – Patient Record Access

This module implements the `access_patient_record` function, which enforces
strict authorization checks to prevent CWE‑284: Improper Access Control.
"""

from typing import Dict, Any

# Example patient records database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        # List of staff IDs who are allowed to view this record
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Monitor blood pressure daily."
        },
    },
    # Additional patient records can be added here
}


def access_patient_record(user_id: str, user_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Return a patient's medical data if the user is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the healthcare professional attempting access.
    user_role : str
        Role of the user. Expected values: 'doctor', 'nurse',
        'admin', or 'receptionist'.
    patient_id : str
        The ID of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    ValueError
        If the patient record does not exist.
    PermissionError
        If the user is not authorized to access the record.

    Notes
    -----
    - Admins have unrestricted access.
    - Doctors and nurses may only view records where they are listed in
      ``assigned_staff``.
    - Receptionists and any other roles are denied access.
    """
    # Retrieve the patient record; raise error if missing
    record = PATIENT_RECORDS.get(patient_id)
    if record is None:
        raise ValueError(f"Patient record '{patient_id}' does not exist.")

    # Normalise role string to avoid case‑sensitivity issues
    role = user_role.strip().lower()

    # Authorization logic
    if role == "admin":
        # Admins bypass all checks
        authorized = True
    elif role in ("doctor", "nurse"):
        # Check if the user is assigned to this patient
        authorized = user_id in record.get("assigned_staff", [])
    else:
        # All other roles are explicitly denied
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized "
            f"to access patient record '{patient_id}'."
        )

    # Return a copy to prevent accidental mutation of the stored data
    return dict(record.get("medical_data", {}))


# Example usage (uncomment to test)
if __name__ == "__main__":
    try:
        data = access_patient_record("doc_123", "doctor", "patient_001")
        print("Access granted. Medical data:", data)
    except Exception as exc:
        print(f"Error: {exc}")