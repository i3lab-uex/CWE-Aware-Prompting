from typing import Dict, List, Any

# Sample patient records store
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_a", "nurse_b"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Amlodipine"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_c"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Allowed roles that can bypass staff assignment check
ALLOWED_ROLES = {"admin", "supervisor"}

def fetch_patient_info(
    staff_identifier: str,
    staff_role: str,
    patient_ref: str
) -> Dict[str, Any]:
    """
    Return the medical data of a patient if the requesting staff member is authorized.

    Raises:
        PermissionError: If the staff member does not have access rights.
        KeyError: If the patient reference is unknown.

    Args:
        staff_identifier (str): The ID of the healthcare personnel.
        staff_role (str): Role of the user ('doctor', 'nurse', 'admin', etc.).
        patient_ref (str): The patient ID whose record is requested.

    Returns:
        dict: Medical data for the patient.
    """
    # Validate input types (basic runtime safety)
    if not isinstance(staff_identifier, str) or not isinstance(staff_role, str) or not isinstance(patient_ref, str):
        raise TypeError("All arguments must be strings")

    # Retrieve patient record
    try:
        record = PATIENT_RECORDS[patient_ref]
    except KeyError as exc:
        # Patient ID not found – expose minimal information
        raise KeyError(f"Patient record '{patient_ref}' does not exist") from exc

    # Authorization check: either staff is assigned or has a privileged role
    if (
        staff_identifier not in record["assigned_staff"]
        and staff_role.lower() not in ALLOWED_ROLES
    ):
        raise PermissionError(
            f"Access denied for staff '{staff_identifier}' with role '{staff_role}' "
            f"to patient '{patient_ref}'."
        )

    # Return a copy to prevent accidental modification of the stored record
    return dict(record["medical_data"])