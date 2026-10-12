# view_patient_record.py

from typing import Dict, Any

# Sample patient records database (in-memory for demonstration)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "treatment_plan": ["Medication A", "Lifestyle changes"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc789"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "treatment_plan": ["Medication B", "Dietary plan"],
        },
    },
}

# Define roles that are allowed to view medical records
ALLOWED_ROLES = {"doctor", "nurse"}

def _is_authorized(staff_id: str, staff_role: str, record: Dict[str, Any]) -> bool:
    """
    Internal helper to check if a staff member is authorized to view the record.
    """
    # Role-based check
    if staff_role.lower() not in ALLOWED_ROLES:
        return False

    # Staff must be assigned to the patient
    if staff_id not in record.get("assigned_staff", []):
        return False

    return True


def view_patient_record(staff_id: str, staff_role: str, patient_record_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Args:
        staff_id (str): Unique identifier of the healthcare professional.
        staff_role (str): Role of the staff member ('doctor', 'nurse', etc.).
        patient_record_id (str): Identifier of the patient record to retrieve.

    Returns:
        dict: The medical data portion of the patient's record.

    Raises:
        KeyError: If the patient_record_id does not exist in PATIENT_RECORDS.
        PermissionError: If the staff member is not authorized to view the record.
    """
    # Fetch patient record
    try:
        record = PATIENT_RECORDS[patient_record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_record_id}' not found.") from exc

    # Authorization check
    if not _is_authorized(staff_id, staff_role, record):
        raise PermissionError(
            f"Staff '{staff_id}' with role '{staff_role}' is not authorized to view patient record '{patient_record_id}'."
        )

    # Return only the medical data
    return record["medical_data"]