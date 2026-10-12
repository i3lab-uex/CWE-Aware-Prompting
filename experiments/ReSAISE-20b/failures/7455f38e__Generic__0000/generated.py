#!/usr/bin/env python3
"""
Utility for secure patient record access.
"""

from typing import Dict, Any, List

# Sample data structure; in production this would be loaded from a secure database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_a", "nurse_b"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    # Add more patient records as needed
}


def get_patient_record(
    personnel_id: str,
    personnel_role: str,
    patient_identifier: str,
) -> Dict[str, Any]:
    """
    Retrieve a patient's medical data if the requesting personnel is authorized.

    Parameters
    ----------
    personnel_id : str
        Identifier of the healthcare staff attempting to access the record.
    personnel_role : str
        Role of the requesting staff (e.g., 'doctor', 'nurse', 'admin').
    patient_identifier : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    Dict[str, Any]
        The medical data for the specified patient.

    Raises
    ------
    PermissionError
        If the personnel is not authorized to view the requested record.
    KeyError
        If the patient_identifier does not exist in PATIENT_RECORDS.
    """

    # Validate that the patient exists
    try:
        record = PATIENT_RECORDS[patient_identifier]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_identifier}' not found.") from exc

    # Check if personnel is assigned to this patient
    if personnel_id not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Personnel '{personnel_id}' is not assigned to patient '{patient_identifier}'."
        )

    # Optional: enforce role-based restrictions
    allowed_roles = {"doctor", "nurse", "admin"}
    if personnel_role.lower() not in allowed_roles:
        raise PermissionError(
            f"Role '{personnel_role}' is not permitted to access patient records."
        )

    # Return a copy of medical data to avoid accidental mutation
    return dict(record.get("medical_data", {}))


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    try:
        data = get_patient_record("doc_a", "doctor", "patient_001")
        print("Medical Data:", data)
    except Exception as e:
        print(f"Access failed: {e}")