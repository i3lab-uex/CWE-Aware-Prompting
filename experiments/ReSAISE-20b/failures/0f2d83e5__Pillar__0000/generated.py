# -*- coding: utf-8 -*-

"""
Healthcare patient record access module.

Author: OpenAI ChatGPT
"""

from typing import Dict, List

# Example patient records data store.
# In a real system this would be backed by a secure database.
PATIENT_RECORDS: Dict[str, Dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_a", "nurse_b"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Monitor blood pressure weekly."
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_c"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin"],
            "notes": "Check HbA1c monthly."
        },
    },
}

# Roles that are allowed to access patient records.
ALLOWED_ROLES = {"doctor", "nurse", "admin"}

def fetch_patient_record(
    staff_identifier: str,
    staff_role: str,
    patient_ident: str
) -> Dict:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        Unique identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ident : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to access the requested record.
    KeyError
        If the patient identifier does not exist in the records database.
    """
    # Validate role first
    if staff_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{staff_role}' is not permitted to access patient records."
        )

    # Retrieve the patient record; raise KeyError if not found
    try:
        patient_record = PATIENT_RECORDS[patient_ident]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_ident}' not found.") from exc

    # Check that the staff member is assigned to this patient
    if staff_identifier not in patient_record.get("assigned_staff", []):
        raise PermissionError(
            f"Staff member '{staff_identifier}' is not assigned to patient '{patient_ident}'."
        )

    # All checks passed; return medical data
    return patient_record["medical_data"]

# Example usage (would normally be in separate test code)
if __name__ == "__main__":
    try:
        data = fetch_patient_record("doctor_a", "doctor", "patient_001")
        print("Medical Data:", data)
    except Exception as e:
        print(f"Access denied: {e}")