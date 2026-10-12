from __future__ import annotations

import typing as _t


# Example patient records structure
PATIENT_RECORDS: dict[str, dict[str, _t.Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["S100", "S101"],  # staff IDs allowed to view
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Amlodipine"]},
    },
    # Add more patient records as needed
}


def review_patient_data(staff_id: str, staff_role: str, patient_id: str) -> dict[str, _t.Any]:
    """
    Allow a healthcare staff member to review a patient's medical data.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare personnel attempting to access the record.
    staff_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier of the patient whose records are being requested.

    Returns
    -------
    dict[str, Any]
        The medical data for the patient if access is authorized.

    Raises
    ------
    PermissionError
        If the user does not have permission to view the patient data.
    KeyError
        If the specified patient_id is not found in PATIENT_RECORDS.
    """
    # Retrieve the patient's record
    patient_record = PATIENT_RECORDS[patient_id]  # KeyError propagates if missing

    # Define roles that have universal access
    UNIVERSAL_ROLES = {"admin"}

    # Authorization logic:
    # - Admins can access any record.
    # - Doctors and nurses must be explicitly assigned to the patient.
    if staff_role in UNIVERSAL_ROLES:
        return patient_record["medical_data"]

    # For other roles, check assignment
    if staff_id in patient_record.get("assigned_staff", []):
        return patient_record["medical_data"]

    # If none of the conditions match, deny access
    raise PermissionError(
        f"Unauthorized access attempt by staff '{staff_id}' "
        f"with role '{staff_role}' to patient '{patient_id}'."
    )