import typing

# Example patient records dictionary.
# In a real application, this would be loaded from a secure database or encrypted store.
PATIENT_RECORDS: dict[str, dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}


def fetch_patient_info(
    staff_identifier: str,
    staff_role: str,
    patient_ref: str,
) -> typing.Any:
    """
    Return the medical data for a patient if access control allows.

    Parameters
    ----------
    staff_identifier : str
        Identifier of the healthcare personnel attempting to access.
    staff_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient reference is unknown.
    """
    # Basic type checks to guard against accidental misuse
    if not all(isinstance(arg, str) for arg in (staff_identifier, staff_role, patient_ref)):
        raise TypeError("All arguments must be strings")

    # Retrieve the patient record; let KeyError propagate if unknown
    patient_record = PATIENT_RECORDS[patient_ref]

    # Admins can view any record
    if staff_role.lower() == "admin":
        return patient_record["medical_data"]

    # Non-admins must be explicitly assigned to the record
    if staff_identifier in patient_record.get("assigned_staff", []):
        return patient_record["medical_data"]

    # If we reach here, access is denied
    raise PermissionError(
        f"Access denied: staff '{staff_identifier}' with role '{staff_role}' "
        f"is not authorized to view patient '{patient_ref}'."
    )