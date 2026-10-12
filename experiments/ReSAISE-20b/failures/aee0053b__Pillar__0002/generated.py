from typing import Dict, Any

# Example patient records store (in a real system this would be secured and encrypted)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": {"doc123", "nurse456"},
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": {"doc789"},
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
    # Additional patient records would be added here...
}


def get_patient_data(staff_num: str, role: str, patient_ref: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Args:
        staff_num (str): ID of the healthcare professional requesting access.
        role (str): Role of the staff member (e.g., 'doctor', 'nurse', 'admin', etc.).
        patient_ref (str): Identifier of the patient whose record is being accessed.

    Returns:
        dict: The patient's medical data.

    Raises:
        KeyError: If the patient_ref does not exist in PATIENT_RECORDS.
        PermissionError: If the staff member is not authorized to access the record.
    """
    # Fetch patient record; let KeyError propagate if not found
    patient_record = PATIENT_RECORDS[patient_ref]

    # Determine authorization:
    # 1. Admin role has blanket access
    # 2. Assigned staff (by ID) have access
    authorized = role.lower() == "admin" or staff_num in patient_record["assigned_staff"]

    if not authorized:
        raise PermissionError(
            f"Staff member '{staff_num}' with role '{role}' is not authorized to access "
            f"patient record '{patient_ref}'."
        )

    # Return a copy of medical data to prevent accidental mutation
    return dict(patient_record["medical_data"])