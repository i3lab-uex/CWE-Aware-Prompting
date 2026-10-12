from typing import Dict, Any

# Sample patient records (normally this would be fetched from a secure database)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_a", "nurse_b"],
        "medical_data": {"diagnosis": "Hypertension", "treatment": "Medication"},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_c"],
        "medical_data": {"diagnosis": "Diabetes", "treatment": "Insulin"},
    },
}

def retrieve_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Retrieve the medical data of a patient if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the patient's record.
    KeyError
        If the patient_id does not exist in PATIENT_RECORDS.
    """
    # Validate patient existence
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_id}' not found.") from exc

    # Define roles that have blanket access
    privileged_roles = {"admin"}

    # Authorization logic:
    # 1. Admins can access any record.
    # 2. Doctors and nurses must be listed in the patient's assigned_staff list.
    if staff_role.lower() in privileged_roles:
        return record["medical_data"]

    # For non-privileged roles, check assignment
    if staff_role.lower() in {"doctor", "nurse"}:
        if staff_id in record["assigned_staff"]:
            return record["medical_data"]

    # All other cases are unauthorized
    raise PermissionError(
        f"Staff '{staff_id}' with role '{staff_role}' is not authorized to access patient '{patient_id}'."
    )