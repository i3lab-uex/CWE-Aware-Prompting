from __future__ import annotations

# Example patient records dictionary. In a real system this would come from a secure database.
PATIENT_RECORDS: dict[str, dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": {"doctor_123", "nurse_456"},
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Patient advised to reduce salt intake."
        },
    },
    # Additional patient records would be listed here.
}


def retrieve_patient_data(
    staff_id: str,
    staff_role: str,
    patient_id: str,
) -> dict:
    """
    Retrieve a patient's medical data if the requesting staff member is authorized.

    Args:
        staff_id: Identifier of the healthcare professional.
        staff_role: Role of the professional (e.g., 'doctor', 'nurse', 'admin').
        patient_id: Identifier of the patient whose record is requested.

    Returns:
        The patient's medical data dictionary.

    Raises:
        PermissionError: If the staff member is not authorized to access the record.
        KeyError: If the patient_id does not exist in PATIENT_RECORDS.
    """
    # Basic role-based access control: only doctors, nurses, and admins may read records.
    allowed_roles = {"doctor", "nurse", "admin"}
    if staff_role.lower() not in allowed_roles:
        raise PermissionError(
            f"Role '{staff_role}' is not permitted to access patient records."
        )

    # Retrieve the patient record; let KeyError propagate if missing.
    record = PATIENT_RECORDS[patient_id]

    # Check that the staff member is listed as assigned to this patient.
    if staff_id not in record.get("assigned_staff", set()):
        raise PermissionError(
            f"Staff ID '{staff_id}' is not assigned to patient '{patient_id}'."
        )

    # All checks passed; return the medical data.
    return record["medical_data"]