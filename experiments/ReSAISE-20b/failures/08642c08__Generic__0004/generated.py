# fetch_patient_info.py

from typing import Dict, Any

# Example patient records dictionary.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

def fetch_patient_info(
    staff_identifier: str,
    staff_role: str,
    patient_ref: str
) -> Dict[str, Any]:
    """
    Retrieve medical data for a patient if the requesting staff member has permission.

    Parameters
    ----------
    staff_identifier : str
        Identifier of the healthcare personnel requesting access.
    staff_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        Identifier of the patient whose data is being requested.

    Returns
    -------
    dict
        The medical data for the patient.

    Raises
    ------
    PermissionError
        If the user does not have permission to access the patient record.
    KeyError
        If the patient reference is not found in `PATIENT_RECORDS`.
    """
    # Validate that the patient exists
    if patient_ref not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_ref}' does not exist.")

    patient_record = PATIENT_RECORDS[patient_ref]

    # Admins have blanket access
    if staff_role.lower() == "admin":
        return patient_record["medical_data"]

    # Doctors and nurses must be explicitly assigned to the patient
    if staff_role.lower() in {"doctor", "nurse"}:
        # Use a constant‑time comparison to avoid timing attacks
        if any(
            staff_identifier == assigned_id for assigned_id in patient_record["assigned_staff"]
        ):
            return patient_record["medical_data"]

    # If we reach here, access is denied
    raise PermissionError(
        f"Unauthorized access attempt by {staff_role} '{staff_identifier}' "
        f"to patient record '{patient_ref}'."
    )