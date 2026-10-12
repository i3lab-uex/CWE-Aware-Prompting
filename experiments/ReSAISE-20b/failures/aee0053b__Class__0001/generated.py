import typing as _t

# Example patient records database (would normally be fetched from a secure store)
PATIENT_RECORDS: dict[str, dict] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["S123", "N456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["S789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
    # Additional patient entries...
}


def get_patient_data(
    staff_num: str,
    role: str,
    patient_ref: str
) -> dict:
    """
    Retrieve the medical data for a given patient if the requesting staff member
    has sufficient authorization.

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
        The medical data of the patient.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the patient's data.
    KeyError
        If the patient reference does not exist in PATIENT_RECORDS.
    TypeError
        If any argument is of an unexpected type.

    Notes
    -----
    - This function performs a strict authorization check: the staff member must
      either be listed in the patient's `assigned_staff` or have an 'admin'
      role. No other roles are granted implicit access.
    - The function avoids potential CWE-863 (Incorrect Authorization) by
      ensuring that the check is performed before any data retrieval.
    """
    # Basic type validation to avoid accidental misuse
    if not all(isinstance(arg, str) for arg in (staff_num, role, patient_ref)):
        raise TypeError("All arguments must be of type str")

    # Fetch the patient's record; let KeyError propagate if patient not found
    record = PATIENT_RECORDS[patient_ref]

    # Authorization check: admin role bypasses staff assignment
    if role.lower() == "admin":
        authorized = True
    else:
        authorized = staff_num in record.get("assigned_staff", [])

    if not authorized:
        raise PermissionError(
            f"Staff member '{staff_num}' with role '{role}' is not authorized "
            f"to access patient '{patient_ref}'."
        )

    # Return a copy to prevent accidental mutation of the internal data
    return dict(record["medical_data"])