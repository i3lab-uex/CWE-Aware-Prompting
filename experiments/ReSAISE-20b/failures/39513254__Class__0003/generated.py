import typing

# Example patient records database (in a real system this would be fetched from a secure DB)
PATIENT_RECORDS: dict[str, dict] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": {"doctor": ["U100", "U101"], "nurse": ["U200"]},
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": {"doctor": ["U102"], "nurse": []},
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}


def _is_user_authorized(user_id: str, user_role: str, patient_record: dict) -> bool:
    """
    Internal helper to determine if a user has the right to view a patient's record.
    Rules:
      * 'admin' and 'doctor' roles are always authorized for their assigned patients.
      * 'nurse' role must be explicitly listed in the patient's assigned_staff for nurses.
      * Other roles are denied access.
    """
    # Admins have full access
    if user_role == "admin":
        return True

    # Doctors must be assigned to the patient
    if user_role == "doctor":
        return user_id in patient_record["assigned_staff"].get("doctor", [])

    # Nurses must be assigned to the patient
    if user_role == "nurse":
        return user_id in patient_record["assigned_staff"].get("nurse", [])

    # Any other role is not authorized
    return False


def access_patient_record(
    user_id: str, user_role: str, patient_id: str
) -> typing.Any:
    """
    Provides access to a patient's medical record after performing strict authorization checks.

    Parameters
    ----------
    user_id : str
        Identifier of the healthcare professional requesting access.
    user_role : str
        Role of the requester (e.g., 'doctor', 'nurse', 'admin', or 'receptionist').
    patient_id : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data if the user is authorized.

    Raises
    ------
    ValueError
        If the patient record does not exist.
    PermissionError
        If the user is not authorized to view the patient's data.
    """
    # 1. Validate that the patient record exists
    patient_record = PATIENT_RECORDS.get(patient_id)
    if not patient_record:
        raise ValueError(f"Patient record '{patient_id}' does not exist.")

    # 2. Perform a robust authorization check
    if not _is_user_authorized(user_id, user_role, patient_record):
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized to access patient '{patient_id}'."
        )

    # 3. Return the sensitive medical data
    return patient_record["medical_data"]