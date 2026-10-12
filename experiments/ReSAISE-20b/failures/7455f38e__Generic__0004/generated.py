from typing import Any, Dict

# Example patient records dictionary.
# In a real system this would be stored securely (e.g., in a database).
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_a", "staff_b"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["staff_c"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}


def get_patient_record(personnel_id: str, personnel_role: str, patient_identifier: str) -> Any:
    """
    Retrieve the medical data for a patient if the requesting personnel has
    sufficient privileges.

    Args:
        personnel_id (str): ID of the healthcare staff requesting access.
        personnel_role (str): Role of the requesting staff
            ('doctor', 'nurse', or 'admin').
        patient_identifier (str): ID of the patient.

    Returns:
        Any: The medical data for the patient.

    Raises:
        KeyError: If the patient_identifier does not exist.
        PermissionError: If access is denied due to insufficient privileges.
    """
    # Ensure the patient exists
    if patient_identifier not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_identifier}' not found.")

    record = PATIENT_RECORDS[patient_identifier]

    # Admins have full access
    if personnel_role.lower() == "admin":
        return record["medical_data"]

    # Doctors and nurses must be assigned to the patient
    if personnel_role.lower() in {"doctor", "nurse"}:
        if personnel_id in record["assigned_staff"]:
            return record["medical_data"]

    # Any other case is unauthorized
    raise PermissionError(
        f"Personnel '{personnel_id}' with role '{personnel_role}' "
        "is not authorized to access this patient record."
    )