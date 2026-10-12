from typing import Dict, Any

# Example patient records store. In a real system this would be in a secure database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    # Additional records can be added here...
}


def view_patient_record(staff_id: str, staff_role: str, patient_record_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record after performing an access control check.

    Args:
        staff_id (str): Unique identifier of the healthcare professional.
        staff_role (str): Role of the staff member ('doctor', 'nurse', 'admin', etc.).
        patient_record_id (str): Identifier of the patient's record to be retrieved.

    Returns:
        dict: The medical data for the requested patient.

    Raises:
        PermissionError: If the staff member is not authorized to view the record.
        KeyError: If the patient_record_id does not exist in PATIENT_RECORDS.
    """
    # Fetch the record; raise KeyError if missing (handled by caller or higher level)
    record = PATIENT_RECORDS[patient_record_id]

    # Basic role-based access: only doctors and nurses may view medical data.
    allowed_roles = {"doctor", "nurse"}
    if staff_role.lower() not in allowed_roles:
        raise PermissionError(f"Role '{staff_role}' is not permitted to view patient records.")

    # Check that the staff member is assigned to this patient
    if staff_id not in record.get("assigned_staff", []):
        raise PermissionError(f"Staff ID '{staff_id}' is not assigned to patient '{patient_record_id}'.")

    # If all checks pass, return the medical data
    return record["medical_data"]