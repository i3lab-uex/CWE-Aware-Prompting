from __future__ import annotations

# Example patient records. In a real system this would be fetched from
# a secure database rather than stored in plain memory.
PATIENT_RECORDS: dict[str, dict] = {
    "P001": {
        "patient_id": "P001",
        # staff identifiers who are allowed to view this record
        "assigned_staff": {"D123", "N456"},
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    # Additional patient records would follow the same structure
}

def fetch_patient_record(
    staff_identifier: str,
    staff_role: str,
    patient_ident: str
) -> dict:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        Unique identifier of the healthcare professional making the request.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ident : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient identifier is unknown.

    Notes
    -----
    * The function implements a simple but explicit authorization check.
      It first verifies that the patient exists, then checks whether the
      staff member is either:
        - listed in the patient's `assigned_staff` set, or
        - has a role that grants universal access (e.g., 'admin').
      This guards against CWE-863 by ensuring the check is performed
      before any data is returned.
    * In a production system, roles and permissions would be managed
      through an RBAC or ABAC system and the patient data would be
      stored in a secure database with encryption at rest.
    """
    # 1. Validate patient existence
    if patient_ident not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_ident}' not found.")

    patient_record = PATIENT_RECORDS[patient_ident]

    # 2. Authorization check
    is_authorized = False

    # Universal access for admins (or other privileged roles)
    if staff_role.lower() == "admin":
        is_authorized = True
    else:
        # Check if staff member is explicitly assigned to the patient
        assigned_staff = patient_record.get("assigned_staff", set())
        if staff_identifier in assigned_staff:
            is_authorized = True

    # 3. Raise error if unauthorized
    if not is_authorized:
        raise PermissionError(
            f"Staff '{staff_identifier}' with role '{staff_role}' "
            f"is not authorized to access patient '{patient_ident}'."
        )

    # 4. Return the medical data
    return patient_record["medical_data"]