from __future__ import annotations

from typing import Dict, Any


# Example patient records database (in practice this would be a secure data store)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": {"doctor_123", "nurse_456"},
        "medical_data": {
            "diagnosis": "Hypertension",
            "treatment_plan": ["Medication A", "Lifestyle changes"],
        },
    },
    # Add more patient records as needed
}


def access_patient_record(
    user_id: str,
    user_role: str,
    patient_id: str,
) -> Dict[str, Any]:
    """
    Return the medical data for a patient if the user is authorized.
    Raises ValueError if the patient record does not exist.

    Args:
        user_id: ID of the healthcare professional attempting access.
        user_role: Role of the user ('doctor', 'nurse', 'admin', or 'receptionist').
        patient_id: ID of the patient whose record is being accessed.

    Returns:
        The patient's medical data dictionary.

    Raises:
        ValueError: If the patient record does not exist.
        PermissionError: If the user is not authorized to access the record.
    """
    # Fetch patient record
    record = PATIENT_RECORDS.get(patient_id)
    if not record:
        raise ValueError(f"Patient record '{patient_id}' does not exist.")

    # Authorization logic
    if user_role == "admin":
        authorized = True
    elif user_role in {"doctor", "nurse"}:
        authorized = user_id in record["assigned_staff"]
    else:  # receptionist or any other role
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized "
            f"to access patient record '{patient_id}'."
        )

    # Return a copy to prevent accidental mutation of the stored data
    return dict(record["medical_data"])


# Example usage (for testing purposes)
if __name__ == "__main__":
    try:
        data = access_patient_record("doctor_123", "doctor", "patient_001")
        print("Access granted:", data)
    except Exception as e:
        print(f"Error: {e}")