from __future__ import annotations

# Custom exception for unauthorized access
class PermissionError(Exception):
    """Raised when a user attempts to access a protected resource without permission."""
    pass


# Example patient records dictionary
PATIENT_RECORDS: dict[str, dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        # Staff IDs that are allowed to view this record
        "assigned_staff": ["doctor_123", "nurse_456"],
        # Sensitive medical data
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}


def fetch_patient_record(
    staff_identifier: str,
    staff_role: str,
    patient_ident: str,
) -> dict:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        The ID of the healthcare professional requesting access.
    staff_role : str
        Role of the healthcare worker (e.g., 'doctor', 'nurse', 'admin').
    patient_ident : str
        The identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient identifier is not found in PATIENT_RECORDS.
    """
    # Ensure the patient exists
    if patient_ident not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_ident}' does not exist.")

    record = PATIENT_RECORDS[patient_ident]

    # Admin role bypasses normal checks
    if staff_role.lower() == "admin":
        return record["medical_data"]

    # For doctors and nurses, check membership in assigned_staff
    if staff_role.lower() in {"doctor", "nurse"}:
        if staff_identifier in record["assigned_staff"]:
            return record["medical_data"]

    # If none of the conditions above are met, deny access
    raise PermissionError(
        f"User '{staff_identifier}' with role '{staff_role}' "
        f"is not authorized to access patient '{patient_ident}'."
    )