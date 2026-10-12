from typing import Dict, Any

# Example patient records dictionary. In a real system this would be loaded from a secure database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "treatment": ["Lisinopril"]},
    },
    # Additional patient entries would be defined here...
}


def fetch_patient_record(staff_identifier: str, staff_role: str, patient_ident: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Args:
        staff_identifier (str): ID of the healthcare professional making the request.
        staff_role (str): Role of the requesting staff member (e.g., 'doctor', 'nurse', 'admin').
        patient_ident (str): Identifier of the patient whose record is requested.

    Returns:
        dict: The patient's medical data.

    Raises:
        PermissionError: If the staff member is not authorized to access the record.
        KeyError: If the patient ID does not exist in PATIENT_RECORDS.
    """
    # Validate patient existence
    try:
        record = PATIENT_RECORDS[patient_ident]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_ident}' not found.") from exc

    # Define roles that are inherently authorized regardless of assignment
    universally_authorized_roles = {"admin", "doctor"}

    # Check if staff has a universal role or is explicitly assigned
    authorized = (
        staff_role.lower() in universally_authorized_roles
        or staff_identifier in record.get("assigned_staff", [])
    )

    if not authorized:
        raise PermissionError(
            f"Access denied for staff '{staff_identifier}' with role '{staff_role}'. "
            "Unauthorized to view patient '{patient_ident}'."
        )

    # Return only the medical data portion
    return record.get("medical_data", {})