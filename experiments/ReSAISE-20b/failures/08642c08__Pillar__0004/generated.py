#!/usr/bin/env python3
"""
Implements a secure patient record access control function.
"""

from typing import Dict, Any

# Example patient records database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

def fetch_patient_info(
    staff_identifier: str,
    staff_role: str,
    patient_ref: str
) -> Dict[str, Any]:
    """
    Return the medical data for a patient if access is authorized.

    Parameters
    ----------
    staff_identifier : str
        Identifier of the healthcare personnel requesting access.
    staff_role : str
        Role of the requester ('doctor', 'nurse', or 'admin').
    patient_ref : str
        Identifier of the patient record to be retrieved.

    Returns
    -------
    dict
        The medical data associated with the patient record.

    Raises
    ------
    PermissionError
        If the requester is not authorized to access the requested record.
    KeyError
        If the patient_ref does not exist in PATIENT_RECORDS.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (staff_identifier, staff_role, patient_ref)):
        raise TypeError("All arguments must be strings.")

    # Fetch the record; let KeyError propagate if patient not found
    record = PATIENT_RECORDS[patient_ref]

    # Define role-based access rules
    if staff_role.lower() == "admin":
        # Admins have unrestricted read access
        return record["medical_data"]

    if staff_role.lower() not in {"doctor", "nurse"}:
        raise PermissionError(f"Role '{staff_role}' is not permitted to access patient data.")

    # Check if the staff member is assigned to this patient
    if staff_identifier not in record["assigned_staff"]:
        raise PermissionError(
            f"Staff member '{staff_identifier}' is not assigned to patient '{patient_ref}'."
        )

    # All checks passed; return the medical data
    return record["medical_data"]


# Example usage (for testing purposes only; remove or guard with __name__ == "__main__")
if __name__ == "__main__":
    try:
        data = fetch_patient_info("doc_123", "doctor", "patient_001")
        print("Access granted:", data)
    except PermissionError as e:
        print("Access denied:", str(e))