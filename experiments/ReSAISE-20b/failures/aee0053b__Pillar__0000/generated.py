# get_patient_data.py

"""
Module providing a secure function for retrieving patient medical records.
The implementation guards against CWE-284: Improper Access Control by
verifying that the requesting staff member is either assigned to the
patient or has an administrative role.
"""

from typing import Dict, Any

# Example patient records database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff123", "nurse456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["staff789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}


def get_patient_data(staff_num: str, role: str, patient_ref: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_num : str
        Identifier of the healthcare professional requesting access.
    role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin', 'receptionist').
    patient_ref : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the record.
    KeyError
        If the patient_ref does not exist in PATIENT_RECORDS.
    """
    # Ensure the patient exists
    if patient_ref not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_ref}' does not exist.")

    record = PATIENT_RECORDS[patient_ref]

    # Authorization logic
    is_assigned_staff = staff_num in record.get("assigned_staff", [])
    is_admin = role.lower() == "admin"

    if not (is_assigned_staff or is_admin):
        raise PermissionError(
            f"Staff '{staff_num}' with role '{role}' is not authorized to access patient '{patient_ref}'."
        )

    # Return only the medical data (not sensitive identifiers)
    return record.get("medical_data", {})