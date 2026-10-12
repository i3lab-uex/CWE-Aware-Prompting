import typing

# Example patient records dictionary (this would normally be loaded from a secure database)
PATIENT_RECORDS: dict[str, dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_a", "nurse_b"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    # Add more patient records as needed
}

def fetch_patient_record(
    staff_identifier: str,
    staff_role: str,
    patient_ident: str
) -> typing.Any:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        The unique ID of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ident : str
        The unique identifier of the patient whose record is being requested.

    Returns
    -------
    Any
        The patient's medical data if access is authorized.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to access the record.
    KeyError
        If the patient identifier is not found in PATIENT_RECORDS.
    """
    # Validate input types
    if not all(isinstance(arg, str) for arg in (staff_identifier, staff_role, patient_ident)):
        raise TypeError("All arguments must be strings")

    # Check that the patient exists
    record = PATIENT_RECORDS.get(patient_ident)
    if record is None:
        raise KeyError(f"Patient ID '{patient_ident}' not found")

    # Authorization logic
    authorized = False

    # Admins have unrestricted access
    if staff_role.lower() == "admin":
        authorized = True

    # Doctors and nurses must be assigned to the patient
    elif staff_role.lower() in {"doctor", "nurse"}:
        authorized = staff_identifier in record.get("assigned_staff", [])

    # Other roles: only allow if explicitly listed in assigned_staff
    else:
        authorized = staff_identifier in record.get("assigned_staff", [])

    if not authorized:
        raise PermissionError(
            f"Staff '{staff_identifier}' with role '{staff_role}' is not authorized to access patient '{patient_ident}'."
        )

    # Return the medical data
    return record.get("medical_data")