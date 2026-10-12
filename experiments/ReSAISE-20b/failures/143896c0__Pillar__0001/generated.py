# -*- coding: utf-8 -*-
"""
Medical record access module.

This module implements a secure function to retrieve patient records
while enforcing strict access control.  The implementation follows
CWE‑284 best practices to prevent unauthorized data exposure.
"""

from typing import Dict, Any

# Example patient records database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Type II Diabetes"],
            "medications": ["Lisinopril 10mg", "Metformin 500mg"],
            "notes": "Patient advised to monitor blood sugar daily."
        },
    },
    # Add more patient records as needed
}


def view_patient_record(staff_id: str, staff_role: str, patient_record_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record after performing authorization checks.

    Parameters
    ----------
    staff_id : str
        Unique identifier of the requesting healthcare professional.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_record_id : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The medical data of the patient.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the record.
    KeyError
        If the patient_record_id does not exist in PATIENT_RECORDS.
    """
    # Verify that the requested record exists
    try:
        record = PATIENT_RECORDS[patient_record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_record_id}' not found.") from exc

    # Only doctors and nurses are allowed to view records
    authorized_roles = {"doctor", "nurse"}
    if staff_role.lower() not in authorized_roles:
        raise PermissionError(
            f"Role '{staff_role}' is not permitted to view patient records."
        )

    # Ensure the staff member is assigned to this patient
    if staff_id not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Staff member '{staff_id}' is not assigned to patient '{patient_record_id}'."
        )

    # All checks passed; return the medical data
    return record["medical_data"]


# Example usage (for demonstration purposes only; remove in production)
if __name__ == "__main__":
    try:
        data = view_patient_record("doc123", "doctor", "patient_001")
        print("Medical Data Retrieved:")
        for key, value in data.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Access denied: {e}")