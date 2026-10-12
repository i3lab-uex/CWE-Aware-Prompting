from typing import Dict, List

# Example patient records dictionary.
PATIENT_RECORDS: Dict[str, Dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_a", "staff_b"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "last_visit": "2024-05-10",
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["staff_c"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin"],
            "last_visit": "2024-04-22",
        },
    },
    # Additional patient records can be added here.
}


def review_patient_data(staff_id: str, staff_role: str, patient_id: str):
    """
    Return medical data for a patient if the staff member has permission to access it.

    Parameters
    ----------
    staff_id : str
        Identifier for the healthcare staff attempting to access the record.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier for the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient_id is not found in PATIENT_RECORDS.
    """
    # Ensure the patient exists
    if patient_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_id}' does not exist.")

    record = PATIENT_RECORDS[patient_id]
    assigned_staff: List[str] = record.get("assigned_staff", [])

    # Admins can view any record
    if staff_role.lower() == "admin":
        return record["medical_data"]

    # Other roles must be explicitly assigned
    if staff_id in assigned_staff:
        return record["medical_data"]

    # If we reach here, access is denied
    raise PermissionError(
        f"Staff '{staff_id}' with role '{staff_role}' is not authorized to access patient '{patient_id}'."
    )