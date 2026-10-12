# access_patient_record.py

from typing import Dict, Any


# Sample patient records dictionary (would normally be loaded from a secure data store)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        # IDs of staff assigned to this patient
        "assigned_staff": {"doctor_a", "nurse_b"},
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": {"doctor_c"},
        "medical_data": {
            "diagnosis": "Diabetes",
            "medications": ["Metformin"],
        },
    },
}


def access_patient_record(user_id: str, user_role: str, patient_id: str) -> Any:
    """
    Allow a healthcare professional to access a patient's medical record after
    performing proper authorization checks.

    Parameters:
        user_id (str): The ID of the professional attempting access.
        user_role (str): Role of the user ('doctor', 'nurse', 'admin',
                         or 'receptionist').
        patient_id (str): The ID of the patient whose record is being accessed.

    Returns:
        Any: The patient's medical data if authorized.

    Raises:
        ValueError: If the patient record does not exist.
        PermissionError: If the user is not authorized to view the record.
    """
    # 1. Verify that the patient exists
    record = PATIENT_RECORDS.get(patient_id)
    if not record:
        raise ValueError(f"Patient record '{patient_id}' does not exist.")

    # 2. Authorization logic
    if user_role == "admin":
        # Admins have unrestricted access
        return record["medical_data"]

    if user_role in {"doctor", "nurse"}:
        # Doctors and nurses may only view records of patients they are assigned to
        if user_id in record.get("assigned_staff", set()):
            return record["medical_data"]

    # All other roles (including receptionist) are denied access
    raise PermissionError(
        f"User '{user_id}' with role '{user_role}' is not authorized to access "
        f"patient '{patient_id}' record."
    )


# Example usage (for testing purposes only; remove or guard with __name__ == "__main__")
if __name__ == "__main__":
    try:
        data = access_patient_record("doctor_a", "doctor", "patient_001")
        print("Access granted. Medical data:", data)
    except Exception as e:
        print(e)