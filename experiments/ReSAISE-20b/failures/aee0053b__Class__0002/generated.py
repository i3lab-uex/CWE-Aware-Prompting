from typing import Dict, List

# Sample patient records database.
PATIENT_RECORDS: Dict[str, Dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        # List of staff IDs assigned to this patient
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Roles that are allowed to read patient data
ALLOWED_ROLES = {"doctor", "nurse", "admin"}


def get_patient_data(staff_num: str, role: str, patient_ref: str) -> Dict:
    """
    Retrieve a patient's medical data if the requesting staff member is authorized.

    Parameters
    ----------
    staff_num : str
        Identifier of the healthcare professional requesting access.
    role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data dictionary.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient_ref is not found in PATIENT_RECORDS.
    """
    # Check that the patient exists
    try:
        record = PATIENT_RECORDS[patient_ref]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_ref}' not found.") from exc

    # Basic role-based check
    if role.lower() not in ALLOWED_ROLES:
        raise PermissionError(f"Role '{role}' is not authorized to access patient records.")

    # Staff assignment check
    if staff_num not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Staff member '{staff_num}' is not assigned to patient '{patient_ref}'."
        )

    # If all checks pass, return the medical data
    return record["medical_data"]