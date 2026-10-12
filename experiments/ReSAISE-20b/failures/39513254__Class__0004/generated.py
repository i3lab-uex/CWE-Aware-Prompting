from __future__ import annotations

# Example patient records. In a real system this would be stored in a secure database.
PATIENT_RECORDS = {
    "patient_001": {
        "patient_id": "patient_001",
        # List of user IDs assigned to this patient
        "assigned_staff": ["doc_a", "nurse_b"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Amlodipine"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_c"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Define roles that have blanket access
ADMIN_ROLES = {"admin"}

def _is_user_authorized(user_id: str, user_role: str, patient_record: dict) -> bool:
    """
    Determine if the user is authorized to view a patient's record.

    - Admins have unrestricted access.
    - Doctors and nurses can view records only if they are in the assigned_staff list.
    - Other roles (e.g., receptionist) have no access.

    Args:
        user_id: ID of the user attempting to access.
        user_role: Role of the user.
        patient_record: The patient's record dictionary.

    Returns:
        True if authorized, False otherwise.
    """
    # Admin role
    if user_role in ADMIN_ROLES:
        return True

    # Doctor or nurse must be assigned to the patient
    if user_role in {"doctor", "nurse"}:
        return user_id in patient_record.get("assigned_staff", [])

    # All other roles are denied
    return False

def access_patient_record(user_id: str, user_role: str, patient_id: str) -> dict:
    """
    Return the medical data of a patient if the user is authorized.

    Raises:
        ValueError: If the patient record does not exist.
        PermissionError: If the user is not authorized to view the record.
    """
    # Validate patient existence
    patient_record = PATIENT_RECORDS.get(patient_id)
    if not patient_record:
        raise ValueError(f"Patient record with ID '{patient_id}' does not exist.")

    # Authorization check
    if not _is_user_authorized(user_id, user_role, patient_record):
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized to access patient '{patient_id}'."
        )

    # Return a copy of the medical data to prevent accidental mutation
    return patient_record["medical_data"].copy()