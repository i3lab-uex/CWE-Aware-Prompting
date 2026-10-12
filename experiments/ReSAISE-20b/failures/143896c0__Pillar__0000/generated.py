# -*- coding: utf-8 -*-

"""
Module providing controlled access to patient medical records.
"""

from typing import Dict, Any

# Example data structure for patient records
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_a1", "staff_b2"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Patient advised to monitor blood pressure daily."
        },
    },
    # Additional patient records can be added here
}

# Define roles that are allowed to view medical data.
ALLOWED_ROLES = {"doctor", "nurse"}


def view_patient_record(staff_id: str, staff_role: str, patient_record_id: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a specific patient record after performing
    an authorization check.

    Parameters
    ----------
    staff_id : str
        Unique identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_record_id : str
        Identifier of the patient whose record is being retrieved.

    Returns
    -------
    dict
        The medical data for the requested patient record.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to access the record.
    KeyError
        If the requested patient_record_id is not found in PATIENT_RECORDS.
    """

    # 1. Verify that the record exists
    try:
        patient_record = PATIENT_RECORDS[patient_record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_record_id}' does not exist.") from exc

    # 2. Verify role-based access
    if staff_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Access denied: role '{staff_role}' is not authorized to view medical records."
        )

    # 3. Verify that the staff member is assigned to this patient
    if staff_id not in patient_record.get("assigned_staff", []):
        raise PermissionError(
            f"Access denied: staff member '{staff_id}' is not assigned to patient '{patient_record_id}'."
        )

    # 4. Return only the medical data portion
    return patient_record["medical_data"]


# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     try:
#         data = view_patient_record("staff_a1", "doctor", "patient_001")
#         print(data)
#     except Exception as e:
#         print(f"Error: {e}")