from typing import Dict, Any

# Example patient records database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        # Staff IDs who are allowed to view this patient's record
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": "Hypertension",
        },
    },
    # Add more patient entries here...
}


def fetch_patient_record(staff_identifier: str, staff_role: str, patient_ident: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Args:
        staff_identifier (str): ID of the healthcare professional requesting access.
        staff_role (str): Role of the professional ('doctor', 'nurse', etc.).
        patient_ident (str): Identifier of the patient.

    Returns:
        dict: The patient's medical data.

    Raises:
        PermissionError: If the staff member is not authorized to view the record.
        KeyError: If the patient identifier does not exist in PATIENT_RECORDS.
    """
    # Ensure the patient exists
    if patient_ident not in PATIENT_RECORDS:
        raise KeyError(f"Patient '{patient_ident}' not found.")

    record = PATIENT_RECORDS[patient_ident]

    # Define which roles are allowed to access medical records
    ALLOWED_ROLES = {"doctor", "nurse"}

    # Check role-based permission
    if staff_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Access denied: role '{staff_role}' is not authorized to view patient records."
        )

    # Check staff identifier-based permission
    if staff_identifier not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Access denied: staff ID '{staff_identifier}' is not assigned to patient '{patient_ident}'."
        )

    # If all checks pass, return the medical data
    return record.get("medical_data", {})