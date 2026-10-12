# -*- coding: utf-8 -*-

"""
Secure patient record access module.
"""

from typing import Dict, List

# Example patient records database
PATIENT_RECORDS: Dict[str, Dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_a", "staff_b"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "treatment_plan": ["Medication A", "Lifestyle changes"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["staff_c"],
        "medical_data": {
            "diagnosis": "Diabetes",
            "treatment_plan": ["Insulin", "Dietary plan"],
        },
    },
}

def review_patient_data(staff_id: str, staff_role: str, patient_id: str) -> dict:
    """
    Return the medical data for a given patient if the requesting staff member
    has proper authorization. Raises PermissionError otherwise.

    Parameters:
        staff_id (str): ID of the healthcare personnel.
        staff_role (str): Role of the personnel ('doctor', 'nurse', 'admin', etc.).
        patient_id (str): ID of the patient.

    Returns:
        dict: The patient's medical data.

    Raises:
        KeyError: If the patient_id does not exist in PATIENT_RECORDS.
        PermissionError: If the staff member is not authorized to view the data.
    """
    # 1. Verify patient exists
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_id}' not found.") from exc

    # 2. Authorization check
    # Admins can view all records
    if staff_role.lower() == "admin":
        return record["medical_data"]

    # Doctors and nurses can view records only if assigned
    if staff_role.lower() in {"doctor", "nurse"}:
        # Use a set for efficient membership test
        assigned = set(record.get("assigned_staff", []))
        if staff_id in assigned:
            return record["medical_data"]

    # Any other role or missing assignment is denied
    raise PermissionError(
        f"Unauthorized access: Staff '{staff_id}' with role '{staff_role}' "
        f"is not permitted to view patient '{patient_id}'."
    )

# Example usage (uncomment for testing):
# try:
#     data = review_patient_data("staff_a", "doctor", "patient_001")
#     print(data)
# except Exception as e:
#     print(e)