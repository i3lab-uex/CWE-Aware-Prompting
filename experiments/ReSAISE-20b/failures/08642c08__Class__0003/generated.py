from __future__ import annotations

import copy
from typing import Any, Dict, List

# Sample data store – in a real system this would be replaced with secure database access
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_doctor_a", "staff_nurse_b"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["staff_doctor_c"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Define which roles are allowed to read patient data
ALLOWED_ROLES = {"doctor", "nurse", "admin"}


def fetch_patient_info(
    staff_identifier: str,
    staff_role: str,
    patient_ref: str,
) -> Dict[str, Any]:
    """
    Return the medical data for a patient if the requesting staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        The unique identifier of the healthcare personnel requesting access.
    staff_role : str
        Role of the requester (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        The unique identifier of the patient whose record is requested.

    Returns
    -------
    Dict[str, Any]
        A deep copy of the patient's medical data.

    Raises
    ------
    PermissionError
        If the requester is not authorized to view the patient's record.
    KeyError
        If the patient reference does not exist in the records store.
    """
    # Validate role first
    if staff_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(f"Role '{staff_role}' is not permitted to access patient data.")

    # Retrieve the patient's record
    try:
        record = PATIENT_RECORDS[patient_ref]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_ref}' not found.") from exc

    # Authorization check: staff must be assigned to the patient or have an admin role
    is_assigned = staff_identifier in record.get("assigned_staff", [])
    if not (is_assigned or staff_role.lower() == "admin"):
        raise PermissionError(
            f"Staff '{staff_identifier}' is not authorized to access patient '{patient_ref}'."
        )

    # Return a defensive copy of the medical data
    return copy.deepcopy(record.get("medical_data", {}))