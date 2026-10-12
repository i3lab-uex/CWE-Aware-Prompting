from typing import Dict, List, Any

# Example patient records dictionary.
# In a real system this would be fetched from a secure database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_a1", "nurse_b2"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "treatment_plan": ["Medication A", "Lifestyle changes"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_c3"],
        "medical_data": {
            "diagnosis": "Diabetes",
            "treatment_plan": ["Insulin therapy", "Dietary plan"],
        },
    },
}


def get_patient_record(
    personnel_id: str,
    personnel_role: str,
    patient_identifier: str,
) -> Any:
    """
    Retrieve a patient's medical data if the requesting personnel is authorized.

    Parameters
    ----------
    personnel_id : str
        Identifier of the healthcare staff attempting access.
    personnel_role : str
        Role of the requesting staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_identifier : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    Any
        The patient's medical data dictionary if access is authorized.

    Raises
    ------
    PermissionError
        If the personnel does not have permission to view the record.
    KeyError
        If the patient_identifier is not found in PATIENT_RECORDS.
    """
    # Validate that the patient exists
    if patient_identifier not in PATIENT_RECORDS:
        raise KeyError(f"Patient '{patient_identifier}' does not exist.")

    record = PATIENT_RECORDS[patient_identifier]

    # Admins have blanket access
    if personnel_role.lower() == "admin":
        return record["medical_data"]

    # Only assigned staff can view the record
    if personnel_id not in record["assigned_staff"]:
        raise PermissionError(
            f"Personnel '{personnel_id}' with role '{personnel_role}' "
            "is not authorized to access this patient record."
        )

    return record["medical_data"]