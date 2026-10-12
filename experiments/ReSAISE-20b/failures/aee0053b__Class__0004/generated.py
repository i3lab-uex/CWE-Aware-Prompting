from typing import Dict, Any

# Example patient records database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_a1", "staff_b2"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["staff_c3"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
    # Additional patient records can be added here
}


def get_patient_data(staff_num: str, role: str, patient_ref: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record for authorized staff.

    Parameters
    ----------
    staff_num : str
        Identifier of the healthcare professional requesting access.
    role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data if access is authorized.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to access the record.
    KeyError
        If the patient_ref is not found in PATIENT_RECORDS.
    """
    # Ensure the patient exists
    if patient_ref not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_ref}' does not exist.")

    patient_record = PATIENT_RECORDS[patient_ref]
    assigned_staff = patient_record.get("assigned_staff", [])

    # Authorization logic
    authorized = False

    # 1. Admin role bypasses staff assignment check
    if role.lower() == "admin":
        authorized = True

    # 2. Check if the staff member is directly assigned to this patient
    elif staff_num in assigned_staff:
        authorized = True

    # 3. Additional roles that may be granted access (e.g., 'doctor' or 'nurse')
    #    For demonstration, we allow doctors and nurses if they are assigned.
    elif role.lower() in {"doctor", "nurse"} and staff_num in assigned_staff:
        authorized = True

    # If still not authorized, raise PermissionError
    if not authorized:
        raise PermissionError(
            f"Staff '{staff_num}' with role '{role}' is not authorized to access patient '{patient_ref}'."
        )

    # Return the medical data
    return patient_record.get("medical_data", {})