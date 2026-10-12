#!/usr/bin/env python3
"""
A minimal access‑controlled patient record viewer.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from typing import Dict, List, Any


# --------------------------------------------------------------------------- #
# Sample patient records. In a real system these would come from a secure DB.
# --------------------------------------------------------------------------- #
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["S123", "S456"],  # staff IDs
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Diabetes"],
            "medications": ["Lisinopril", "Metformin"],
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["S789"],
        "medical_data": {
            "name": "Jane Smith",
            "age": 30,
            "diagnosis": ["Asthma"],
            "medications": ["Albuterol"],
        },
    },
}


def review_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Return a patient's medical data if the staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare personnel requesting access.
    staff_role : str
        Role of the requester (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier of the patient whose data is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the requester is not authorized to view the data.
    KeyError
        If the patient_id does not exist in PATIENT_RECORDS.
    """
    # Validate input types
    if not isinstance(staff_id, str) or not isinstance(staff_role, str) or not isinstance(patient_id, str):
        raise TypeError("All arguments must be strings")

    # Retrieve patient record
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:  # patient not found
        raise KeyError(f"Patient ID {patient_id!r} does not exist") from exc

    # Admins have full access
    if staff_role.lower() == "admin":
        return record["medical_data"]

    # For non-admins, check if staff is explicitly assigned
    if staff_id in record["assigned_staff"]:
        return record["medical_data"]

    # No permission
    raise PermissionError(
        f"Staff {staff_id!r} with role '{staff_role}' is not authorized to view patient {patient_id}"
    )


# --------------------------------------------------------------------------- #
# Example usage (uncomment for manual testing)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        data = review_patient_data("S123", "doctor", "P001")
        print("Medical Data:", data)
    except Exception as e:
        print(f"Access denied: {e}")