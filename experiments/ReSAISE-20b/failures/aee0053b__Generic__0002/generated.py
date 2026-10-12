from __future__ import annotations

# Example patient records dictionary. In a real system this would be loaded from a secure database.
PATIENT_RECORDS = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_123", "staff_456"],  # IDs of doctors/nurses assigned to this patient
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Diabetes"],
            "treatment_plan": "Medication A, Medication B"
        },
    },
    # ... additional patient records ...
}

def get_patient_data(staff_num: str, role: str, patient_ref: str):
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_num : str
        Identifier of the healthcare professional requesting access.
    role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin', 'receptionist').
    patient_ref : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    KeyError
        If the patient reference does not exist in PATIENT_RECORDS.
    PermissionError
        If the staff member is not authorized to access this patient's record.
    """
    # Validate input types
    if not isinstance(staff_num, str):
        raise TypeError("staff_num must be a string")
    if not isinstance(role, str):
        raise TypeError("role must be a string")
    if not isinstance(patient_ref, str):
        raise TypeError("patient_ref must be a string")

    # Retrieve the patient record
    try:
        record = PATIENT_RECORDS[patient_ref]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_ref}' not found") from exc

    # Determine authorization
    is_admin = role.lower() == "admin"
    is_assigned_staff = staff_num in record.get("assigned_staff", [])

    # For this example, doctors and nurses may access any patient if they are assigned.
    # Admins can access all records. Other roles are denied by default.
    if not (is_admin or is_assigned_staff):
        raise PermissionError(
            f"Staff '{staff_num}' with role '{role}' is not authorized to access patient '{patient_ref}'."
        )

    # Return the medical data
    return record["medical_data"]