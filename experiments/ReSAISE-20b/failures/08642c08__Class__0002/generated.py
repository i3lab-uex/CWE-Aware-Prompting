from typing import Dict, List, Any

# Example patient records database (for illustration only)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Monitor blood pressure weekly."
        },
    },
    # Additional patient records would be added here
}

def fetch_patient_info(
    staff_identifier: str,
    staff_role: str,
    patient_ref: str
) -> Dict[str, Any]:
    """
    Retrieve the medical data for a specified patient if the requesting staff
    has appropriate authorization.

    Parameters:
        staff_identifier (str): ID of the healthcare personnel.
        staff_role (str): Role of the requesting staff ('doctor', 'nurse', 'admin', etc.).
        patient_ref (str): ID of the target patient.

    Returns:
        dict: The patient's medical data.

    Raises:
        PermissionError: If the staff is not authorized to access the record.
        KeyError: If the patient reference does not exist in PATIENT_RECORDS.
    """
    # Ensure the patient record exists
    if patient_ref not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_ref}' does not exist.")

    patient_record = PATIENT_RECORDS[patient_ref]
    assigned_staff: List[str] = patient_record.get("assigned_staff", [])

    # Authorization logic:
    # 1. Admins have universal access.
    # 2. Staff must be explicitly listed in assigned_staff for non-admin roles.
    if staff_role.lower() == "admin":
        authorized = True
    else:
        # Use a set for efficient lookup; converting list to set each time is inexpensive here.
        authorized = staff_identifier in set(assigned_staff)

    if not authorized:
        raise PermissionError(
            f"Unauthorized access attempt by staff '{staff_identifier}' "
            f"(role: {staff_role}) to patient '{patient_ref}'."
        )

    # Return a copy of the medical data to prevent accidental mutation
    return dict(patient_record.get("medical_data", {}))