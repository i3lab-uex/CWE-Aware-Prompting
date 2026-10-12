# -*- coding: utf-8 -*-
"""
Healthcare patient record access module.

Provides a secure function to fetch medical data for patients
only when the requesting staff member is authorized.
"""

from typing import Dict, Any

# Sample patient records (would normally come from a database)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["D123", "N456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["D789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}


def fetch_patient_record(staff_identifier: str, staff_role: str, patient_ident: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        The unique ID of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin', 'receptionist').
    patient_ident : str
        The unique ID of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to access the record.
    KeyError
        If the patient identifier is not found in PATIENT_RECORDS.
    """
    # 1. Validate patient existence
    if patient_ident not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_ident}' does not exist.")

    record = PATIENT_RECORDS[patient_ident]

    # 2. Determine authorization
    authorized = False

    # Admins can access all records
    if staff_role.lower() == "admin":
        authorized = True

    # Doctors and nurses must be explicitly assigned to the patient
    elif staff_role.lower() in {"doctor", "nurse"}:
        if staff_identifier in record.get("assigned_staff", []):
            authorized = True

    # Other roles are not permitted to view medical data
    else:
        authorized = False

    if not authorized:
        raise PermissionError(
            f"Staff '{staff_identifier}' with role '{staff_role}' is not authorized "
            f"to access patient record '{patient_ident}'."
        )

    # 3. Return the medical data
    return record["medical_data"]


# Example usage (commented out; remove comments to test)
# if __name__ == "__main__":
#     try:
#         data = fetch_patient_record("D123", "doctor", "P001")
#         print("Medical Data:", data)
#     except Exception as e:
#         print("Error:", e)