# -*- coding: utf-8 -*-
"""
Patient record access module.

This module provides a single function `view_patient_record` that allows
healthcare staff to retrieve medical data for a patient, while enforcing
proper access control.  The function checks that the requesting staff member
is either explicitly assigned to the patient record or has an administrative
role.  Unauthorized access raises a `PermissionError`.

Author: OpenAI ChatGPT
"""

from typing import Dict, Any

# Sample patient records database.
# In a real system this would be replaced by secure persistent storage
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "treatment_plan": ["Medication A", "Lifestyle changes"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_789"],
        "medical_data": {
            "diagnosis": "Diabetes",
            "treatment_plan": ["Insulin therapy"],
        },
    },
}


def view_patient_record(
    staff_id: str,
    staff_role: str,
    patient_record_id: str,
) -> Dict[str, Any]:
    """
    Retrieve the medical data for a patient record if the staff member is
    authorized.

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
        The medical data for the requested patient record.

    Raises
    ------
    KeyError
        If the `patient_record_id` does not exist in PATIENT_RECORDS.
    PermissionError
        If the staff member is not authorized to view the record.
    """
    # 1. Retrieve the patient record; raise KeyError if not found
    try:
        record = PATIENT_RECORDS[patient_record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_record_id}' not found.") from exc

    # 2. Authorization logic
    #   - Admins have blanket access.
    #   - Otherwise, staff must be listed in the record's `assigned_staff`.
    if staff_role.lower() == "admin":
        authorized = True
    else:
        authorized = staff_id in record.get("assigned_staff", [])

    if not authorized:
        raise PermissionError(
            f"Staff member '{staff_id}' with role '{staff_role}' "
            "is not authorized to view this patient record."
        )

    # 3. Return the medical data
    return record.get("medical_data", {})


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         data = view_patient_record("doctor_123", "doctor", "patient_001")
#         print(data)
#     except Exception as e:
#         print(e)