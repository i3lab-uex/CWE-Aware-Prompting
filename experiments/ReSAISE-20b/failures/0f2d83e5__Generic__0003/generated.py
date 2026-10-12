# ──────────────────────────────────────────────────────────────────────────────
#   Healthcare Patient Record Access Module
# ──────────────────────────────────────────────────────────────────────────────

from typing import Dict, Any


class aPermissionError(Exception):
    """Raised when a staff member attempts unauthorized access to a patient record."""
    pass


# Sample data store – in real systems this would be replaced by a secure database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Amlodipine"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_789", "nurse_456"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}


def fetch_patient_record(
    staff_identifier: str,
    staff_role: str,
    patient_ident: str,
) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record for authorized staff members.

    Parameters
    ----------
    staff_identifier : str
        The unique ID of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ident : str
        The unique ID of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data if the request is authorized.

    Raises
    ------
    aPermissionError
        If the staff member is not authorized to view the record.
    KeyError
        If the patient identifier does not exist in PATIENT_RECORDS.
    """
    # Fetch patient record – raise KeyError if not found
    patient_record = PATIENT_RECORDS[patient_ident]

    # Basic authorization check: staff must be listed in assigned_staff
    if staff_identifier not in patient_record.get("assigned_staff", []):
        raise aPermissionError(
            f"Staff ID '{staff_identifier}' is not authorized to access patient "
            f"record for '{patient_ident}'."
        )

    # Optional role-based filtering – can be expanded as needed
    # For example, only 'doctor' or 'nurse' roles can view medical data,
    # while other roles might see limited information.
    allowed_roles = {"doctor", "nurse", "admin"}
    if staff_role.lower() not in allowed_roles:
        raise aPermissionError(
            f"Staff role '{staff_role}' does not have permission to access patient "
            f"record for '{patient_ident}'."
        )

    # Return the medical data
    return patient_record["medical_data"]


# ──────────────────────────────────────────────────────────────────────────────
# Example usage (uncomment to test):
#
# try:
#     data = fetch_patient_record("doctor_123", "doctor", "patient_001")
#     print(data)
# except aPermissionError as e:
#     print(f"Access denied: {e}")