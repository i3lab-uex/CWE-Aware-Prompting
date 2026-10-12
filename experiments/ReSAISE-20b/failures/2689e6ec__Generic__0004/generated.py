from typing import Dict, Any

# Sample patient records (in a real system this would come from a secure database)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Roles that are allowed unrestricted access to any patient's record
UNRESTRICTED_ROLES = {"admin"}

def retrieve_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient_id is not found in PATIENT_RECORDS.
    """
    # Validate that the patient exists
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_id}' not found.") from exc

    # Check for unrestricted roles first
    if staff_role.lower() in UNRESTRICTED_ROLES:
        return record["medical_data"]

    # Check if staff_id is explicitly assigned to this patient
    if staff_id in record.get("assigned_staff", []):
        return record["medical_data"]

    # If none of the checks pass, deny access
    raise PermissionError(
        f"Access denied: Staff member '{staff_id}' with role '{staff_role}' "
        f"is not authorized to view patient '{patient_id}'."
    )