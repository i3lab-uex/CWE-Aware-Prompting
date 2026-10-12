from typing import Dict, Any

# Sample patient records store
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        # List of staff identifiers allowed to view this record
        "assigned_staff": ["doc_123", "nurse_456"],
        # Sensitive medical data
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril 10mg"],
            "notes": "Monitor blood pressure daily."
        },
    },
    # Additional patient entries can be added here
}

def fetch_patient_info(
    staff_identifier: str,
    staff_role: str,
    patient_ref: str
) -> Dict[str, Any]:
    """
    Return medical data for a patient if the staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        Unique identifier of the healthcare staff.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        Identifier of the patient.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to access the record.
    KeyError
        If the patient reference does not exist in PATIENT_RECORDS.
    """
    # Ensure the patient exists
    try:
        record = PATIENT_RECORDS[patient_ref]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_ref}' not found.") from exc

    # Authorization: staff must be in assigned_staff list
    if staff_identifier not in record.get("assigned_staff", []):
        # Additional check: admins may override
        if staff_role.lower() != "admin":
            raise PermissionError(
                f"Unauthorized access by {staff_identifier} ({staff_role}) to patient '{patient_ref}'."
            )

    # Return a copy to prevent accidental mutation
    return record["medical_data"].copy()