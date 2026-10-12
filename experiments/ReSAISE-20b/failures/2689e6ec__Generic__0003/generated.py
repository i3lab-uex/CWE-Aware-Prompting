from typing import Dict, Any

# Example patient records dictionary. In a real system this would come from a secure database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

def retrieve_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a specified patient if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        The unique identifier of the healthcare professional requesting access.
    staff_role : str
        The role of the healthcare worker (e.g., 'doctor', 'nurse', 'admin', 'receptionist').
    patient_id : str
        The identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data if access is authorized.

    Raises
    ------
    KeyError
        If the patient_id does not exist in PATIENT_RECORDS.
    PermissionError
        If the staff member is not authorized to view the patient's data.
    """
    # Retrieve patient record, raising KeyError if not found
    patient_record = PATIENT_RECORDS[patient_id]

    # Determine authorization based on role and assignment
    authorized = False

    # Admins have universal access
    if staff_role.lower() == "admin":
        authorized = True

    # Doctors and nurses may only access records of patients assigned to them
    elif staff_role.lower() in {"doctor", "nurse"}:
        if staff_id in patient_record["assigned_staff"]:
            authorized = True

    # Other roles are not permitted to view medical data
    else:
        authorized = False

    if not authorized:
        raise PermissionError(
            f"Access denied: staff_id '{staff_id}' with role '{staff_role}' "
            f"is not authorized to view patient '{patient_id}'."
        )

    return patient_record["medical_data"]