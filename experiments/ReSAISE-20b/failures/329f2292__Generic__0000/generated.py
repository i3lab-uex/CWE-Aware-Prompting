from typing import Dict, List, Any

# Example patient records database.
# In a real application this would be fetched from a secure database or service.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_a", "nurse_b"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril 10mg"],
            "lab_results": {"blood_pressure": "140/90"},
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_c"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin 500mg"],
            "lab_results": {"HbA1c": "7.2%"},
        },
    },
}


def review_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a patient if the staff member has proper access rights.

    Parameters
    ----------
    staff_id : str
        Identifier for the healthcare personnel requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier of the patient whose data is requested.

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
    # Validate that the patient exists
    if patient_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_id}' does not exist.")

    record = PATIENT_RECORDS[patient_id]

    # Admins have blanket access
    if staff_role.lower() == "admin":
        return record["medical_data"]

    # Doctors and nurses must be explicitly assigned to the patient
    if staff_id in record["assigned_staff"]:
        return record["medical_data"]

    # Any other role without explicit assignment is denied
    raise PermissionError(
        f"Access denied for staff '{staff_id}' with role '{staff_role}' "
        f"to patient record '{patient_id}'."
    )