from typing import Dict, Any

# Example patient records database.
# In a real system this would be fetched from a secure database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_a", "nurse_b"],
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": "Hypertension",
            "treatment_plan": ["Lisinopril", "Low-sodium diet"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_c"],
        "medical_data": {
            "name": "Jane Smith",
            "age": 30,
            "diagnosis": "Asthma",
            "treatment_plan": ["Albuterol", "Inhaler"],
        },
    },
}


def view_patient_record(
    staff_id: str,
    staff_role: str,
    patient_record_id: str,
) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record after performing an authorization check.

    Parameters
    ----------
    staff_id : str
        Unique identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_record_id : str
        Identifier of the patient record to retrieve.

    Returns
    -------
    dict
        The medical data for the requested patient.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient_record_id is not found in PATIENT_RECORDS.
    """
    # Ensure the record exists
    if patient_record_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_record_id}' does not exist.")

    record = PATIENT_RECORDS[patient_record_id]

    # Admins have unrestricted access
    if staff_role.lower() == "admin":
        return record["medical_data"]

    # Non-admins must be assigned to the patient
    if staff_id in record["assigned_staff"]:
        return record["medical_data"]

    # If none of the above, deny access
    raise PermissionError(
        f"Staff member '{staff_id}' with role '{staff_role}' "
        f"is not authorized to view patient record '{patient_record_id}'."
    )