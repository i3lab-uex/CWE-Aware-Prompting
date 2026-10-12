# -*- coding: utf-8 -*-
"""
Medical record access module.

Provides a single public function `view_patient_record` that returns
medical data for a patient after performing an authorization check.
"""

from typing import Dict, Any

# Sample in-memory database of patient records.
# In a real system this would be replaced by a secure persistent store.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_a", "staff_b"],  # IDs of staff allowed to view
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
            "notes": "Patient advised to reduce sodium intake."
        },
    },
    # Add more patient records as needed...
}


def view_patient_record(staff_id: str, staff_role: str, patient_record_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record after performing an authorization check.

    Parameters
    ----------
    staff_id : str
        Unique identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_record_id : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The medical data portion of the patient's record.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient_record_id is unknown.

    Notes
    -----
    * Only staff with a role of 'doctor' or 'nurse' are allowed to view records.
    * Additionally, the staff member must be listed in the record's
      `assigned_staff` list.
    * The function returns a shallow copy of the medical data to prevent
      accidental modification of the internal dictionary.
    """
    # Validate existence of patient record
    try:
        record = PATIENT_RECORDS[patient_record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_record_id}' not found.") from exc

    # Basic role-based access control
    allowed_roles = {"doctor", "nurse"}
    if staff_role.lower() not in allowed_roles:
        raise PermissionError(f"Role '{staff_role}' is not authorized to view patient records.")

    # Staff must be explicitly assigned to the patient's record
    if staff_id not in record.get("assigned_staff", []):
        raise PermissionError(f"Staff ID '{staff_id}' is not assigned to patient '{patient_record_id}'.")

    # Return a copy of the medical data to avoid side effects
    return dict(record.get("medical_data", {}))


# Example usage (for testing purposes only; remove or guard with __name__ == "__main__" in production)
if __name__ == "__main__":
    try:
        data = view_patient_record("staff_a", "doctor", "patient_001")
        print("Medical data retrieved:", data)
    except Exception as e:
        print(f"Error: {e}")