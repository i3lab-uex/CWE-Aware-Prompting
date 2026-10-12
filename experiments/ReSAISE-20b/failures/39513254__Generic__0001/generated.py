# access_patient_record.py

from typing import Dict, Any


# Example patient records structure.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["U100", "U101"],  # doctor and nurse IDs
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["U102"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
    # ... more records
}


def access_patient_record(user_id: str, user_role: str, patient_id: str) -> Any:
    """
    Allows a healthcare professional to access a patient's medical record after
    performing authorization checks.

    Parameters:
        user_id (str): ID of the healthcare professional.
        user_role (str): Role of the user ('doctor', 'nurse', 'admin', or others).
        patient_id (str): ID of the patient whose record is requested.

    Returns:
        Any: The medical data dictionary for the specified patient.

    Raises:
        ValueError: If the patient record does not exist.
        PermissionError: If the user is not authorized to access the record.
    """
    # 1. Verify that the patient exists
    if patient_id not in PATIENT_RECORDS:
        raise ValueError(f"Patient record '{patient_id}' does not exist.")

    patient_record = PATIENT_RECORDS[patient_id]

    # 2. Authorization logic
    # Admins can view all records
    if user_role.lower() == "admin":
        return patient_record["medical_data"]

    # Doctors and nurses can view records only if assigned
    if user_role.lower() in {"doctor", "nurse"}:
        if user_id in patient_record.get("assigned_staff", []):
            return patient_record["medical_data"]

    # All other roles are not authorized
    raise PermissionError(
        f"User '{user_id}' with role '{user_role}' is not authorized to access patient '{patient_id}'."
    )