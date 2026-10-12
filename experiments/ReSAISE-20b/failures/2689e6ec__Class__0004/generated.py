from typing import Dict, Any

# Example patient records database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": {"doctor": ["D123"], "nurse": ["N456"]},
        "medical_data": {"diagnosis": "Hypertension", "treatment": "Medication"},
    },
    # Add more patient records as needed...
}

def retrieve_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical data if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin', 'receptionist').
    patient_id : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to access the patient's record.
    KeyError
        If the patient_id does not exist in PATIENT_RECORDS.
    """
    # Ensure the patient exists
    if patient_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_id}' not found.")

    record = PATIENT_RECORDS[patient_id]

    # Admins have full access
    if staff_role.lower() == "admin":
        return record["medical_data"]

    # For doctors and nurses, check if staff_id is in the assigned list
    role_key = staff_role.lower()
    assigned_staff = record.get("assigned_staff", {})
    if role_key in assigned_staff and staff_id in assigned_staff[role_key]:
        return record["medical_data"]

    # Other roles are not permitted
    raise PermissionError(
        f"Staff member '{staff_id}' with role '{staff_role}' is not authorized "
        f"to access patient '{patient_id}'."
    )