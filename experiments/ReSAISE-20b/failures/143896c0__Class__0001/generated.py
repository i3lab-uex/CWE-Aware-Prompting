# -*- coding: utf-8 -*-
"""
A minimal, self‑contained implementation of a patient record access
function that guards against incorrect authorization (CWE‑863).
"""

from __future__ import annotations

import typing as _t
from dataclasses import dataclass, field

# --------------------------------------------------------------------------- #
# Sample data structures (would normally come from a secure database)
# --------------------------------------------------------------------------- #

@dataclass
class PatientRecord:
    patient_id: str
    assigned_staff: _t.Set[str]  # set of staff IDs who may view the record
    medical_data: _t.Dict[str, _t.Any]  # the actual patient information

# Example repository of patient records
PATIENT_RECORDS: _t.Dict[str, PatientRecord] = {
    "patient_001": PatientRecord(
        patient_id="patient_001",
        assigned_staff={"doc123", "nurse456"},
        medical_data={
            "name": "John Doe",
            "age": 45,
            "diagnosis": "Hypertension",
        },
    ),
    # Add more records as needed...
}

# --------------------------------------------------------------------------- #
# Authorization helpers
# --------------------------------------------------------------------------- #

def _is_staff_authorized(
    staff_id: str,
    patient_record: PatientRecord,
) -> bool:
    """
    Check whether a staff member is permitted to view the given patient record.
    The check is intentionally simple: a staff ID must be present in the
    assigned_staff set of the record.
    """
    # In a real system, more sophisticated checks would be performed
    return staff_id in patient_record.assigned_staff


# --------------------------------------------------------------------------- #
# Main API function
# --------------------------------------------------------------------------- #

def view_patient_record(
    staff_id: str,
    staff_role: str,  # role is currently unused but kept for future expansion
    patient_record_id: str,
) -> _t.Dict[str, _t.Any]:
    """
    Retrieve the medical data for a patient record after performing an
    authorization check.

    Parameters
    ----------
    staff_id : str
        Unique identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_record_id : str
        Identifier of the patient record to be retrieved.

    Returns
    -------
    dict
        The medical data contained in the patient record.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the requested record.
    KeyError
        If the patient_record_id does not exist in PATIENT_RECORDS.
    """
    # 1. Validate existence of the record
    try:
        patient_record = PATIENT_RECORDS[patient_record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_record_id}' not found.") from exc

    # 2. Perform the authorization check
    if not _is_staff_authorized(staff_id, patient_record):
        raise PermissionError(
            f"Staff member '{staff_id}' does not have permission "
            f"to view patient record '{patient_record_id}'."
        )

    # 3. Return the medical data
    return patient_record.medical_data


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Should succeed
    print(view_patient_record("doc123", "doctor", "patient_001"))

    # Should fail (unauthorized staff)
    try:
        view_patient_record("nurse999", "nurse", "patient_001")
    except PermissionError as e:
        print(e)