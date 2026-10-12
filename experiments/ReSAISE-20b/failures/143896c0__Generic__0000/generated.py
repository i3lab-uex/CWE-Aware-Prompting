from __future__ import annotations

import typing as _t

# Example patient records structure:
# PATIENT_RECORDS = {
#     "patient1": {
#         "patient_id": "patient1",
#         "assigned_staff": {"doctor_123", "nurse_456"},
#         "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
#     },
#     ...
# }

PATIENT_RECORDS: dict[str, dict] = {}


def view_patient_record(
    staff_id: str,
    staff_role: str,
    patient_record_id: str,
) -> dict:
    """
    Retrieve the medical data for a specific patient record.

    Parameters
    ----------
    staff_id : str
        Unique identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_record_id : str
        Identifier of the patient record to retrieve.

    Returns
    -------
    dict
        The medical data for the specified patient.

    Raises
    ------
    KeyError
        If no record with ``patient_record_id`` exists.
    PermissionError
        If the staff member is not authorized to view the record.
    """
    # Ensure the record exists
    try:
        record = PATIENT_RECORDS[patient_record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_record_id}' not found.") from exc

    # Authorization logic
    # Admins can access all records.
    if staff_role.lower() == "admin":
        return record["medical_data"]

    # Doctors and nurses can access records only if they are assigned.
    assigned_staff: _t.Set[str] = record.get("assigned_staff", set())
    if staff_id in assigned_staff:
        return record["medical_data"]

    # If none of the above, deny access
    raise PermissionError(
        f"Staff '{staff_id}' with role '{staff_role}' is not authorized to view "
        f"patient record '{patient_record_id}'."
    )