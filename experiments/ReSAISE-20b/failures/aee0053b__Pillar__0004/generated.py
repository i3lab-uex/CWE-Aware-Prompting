from __future__ import annotations

from typing import Dict, Any

# Sample patient records database. In a real system this would be replaced by
# secure persistent storage (e.g., an encrypted database).
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient001": {
        "patient_id": "patient001",
        # list of staff IDs that are allowed to view this record
        "assigned_staff": ["staffA", "staffB"],
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Diabetes"],
        },
    },
    # ... more records ...
}

# Roles that are allowed to access medical data. In a real application
# this would be derived from a role‑based access control policy.
ALLOWED_ROLES = {"doctor", "nurse", "admin"}


def get_patient_data(staff_num: str, role: str, patient_ref: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_num : str
        Identifier of the healthcare professional requesting access.
    role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The medical data of the patient.

    Raises
    ------
    KeyError
        If the patient reference does not exist.
    PermissionError
        If the staff member is not authorized to access the record.
    """
    # 1. Validate patient existence
    if patient_ref not in PATIENT_RECORDS:
        raise KeyError(f"Patient reference '{patient_ref}' not found.")

    record = PATIENT_RECORDS[patient_ref]

    # 2. Check role validity
    if role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{role}' is not authorized to access patient data."
        )

    # 3. Verify that the staff member is assigned to this patient
    if staff_num not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Staff member '{staff_num}' is not assigned to patient '{patient_ref}'."
        )

    # 4. Return the sensitive medical data
    return record["medical_data"]