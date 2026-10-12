from typing import Dict, Any

# Sample patient records data structure.
# In a real system this would be fetched from a secure database or API.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_a", "staff_b"],  # staff IDs who can access
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Monitor blood pressure daily."
        },
    },
    # Additional patient records...
}


def view_patient_record(staff_id: str, staff_role: str, patient_record_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Unique identifier of the healthcare professional requesting the record.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_record_id : str
        Identifier of the patient whose record is being retrieved.

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
    # Fetch the record; KeyError will propagate if missing
    record = PATIENT_RECORDS[patient_record_id]

    # Authorization logic:
    # 1. Admins can view all records.
    # 2. Staff assigned to the patient can view the record.
    if staff_role.lower() == "admin":
        authorized = True
    else:
        # Ensure assigned_staff exists and is a list to avoid type errors.
        assigned = record.get("assigned_staff", [])
        authorized = staff_id in assigned

    if not authorized:
        # Raise a PermissionError with a clear message.
        raise PermissionError(
            f"Staff member '{staff_id}' (role: {staff_role}) "
            f"is not authorized to view record '{patient_record_id}'."
        )

    # Return only the medical data portion of the record.
    return record["medical_data"]