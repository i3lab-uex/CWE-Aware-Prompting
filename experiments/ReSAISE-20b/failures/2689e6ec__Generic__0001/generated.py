from typing import Dict, Any

# Example patient records database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "treatment": "Medication A"},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_789"],
        "medical_data": {"diagnosis": "Diabetes", "treatment": "Insulin"},
    },
    # Add more patient records as needed
}

# Roles that are automatically granted access regardless of assignment.
ALWAYS_AUTHORIZED_ROLES = {"admin"}

def retrieve_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Retrieve the medical data of a patient if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the professional (e.g., 'doctor', 'nurse', 'admin', 'receptionist').
    patient_id : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the record.
    KeyError
        If the patient_id does not exist in PATIENT_RECORDS.
    """
    # Validate that the patient exists
    if patient_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_id}' not found.")

    record = PATIENT_RECORDS[patient_id]

    # Determine authorization
    is_authorized = False

    # Admins have blanket access
    if staff_role.lower() in ALWAYS_AUTHORIZED_ROLES:
        is_authorized = True

    # Assigned staff members (doctor/nurse) have access
    elif staff_id in record.get("assigned_staff", []):
        is_authorized = True

    # Additional role-based checks can be added here if needed

    if not is_authorized:
        raise PermissionError(
            f"Staff '{staff_id}' with role '{staff_role}' is not authorized to access patient '{patient_id}'."
        )

    # Return a copy to prevent accidental modifications
    return dict(record["medical_data"])