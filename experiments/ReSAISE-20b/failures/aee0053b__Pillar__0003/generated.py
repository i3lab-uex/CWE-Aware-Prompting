# -*- coding: utf-8 -*-

"""
Module providing secure access to patient records.
"""

from typing import Dict, Any

# Example patient record store. In production this would be replaced by a secure database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["S123", "S456"],  # staff numbers authorized for this patient
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": "Hypertension",
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["S789"],
        "medical_data": {
            "name": "Jane Smith",
            "age": 32,
            "diagnosis": "Asthma",
        },
    },
}


def get_patient_data(staff_num: str, role: str, patient_ref: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Args:
        staff_num (str): Identifier of the healthcare professional making the request.
        role (str): Role of the requesting staff member, e.g., 'doctor', 'nurse', 'admin'.
        patient_ref (str): Identifier of the patient whose record is being accessed.

    Returns:
        dict: The patient's medical data.

    Raises:
        PermissionError: If the staff member does not have permission to access the record.
        KeyError: If the patient reference is unknown.

    Notes:
        - This function implements a simple role‑based and ownership check to mitigate
          CWE-284 (Improper Access Control). In a real system, authentication tokens,
          audit logs and more granular permissions would be used.
    """
    # 1. Verify patient exists
    try:
        record = PATIENT_RECORDS[patient_ref]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_ref}' not found.") from exc

    # 2. Check authorization
    is_admin = role.lower() == "admin"
    is_assigned_staff = staff_num in record.get("assigned_staff", [])

    if not (is_admin or is_assigned_staff):
        raise PermissionError(
            f"Staff member '{staff_num}' with role '{role}' is not authorized "
            f"to access patient '{patient_ref}'."
        )

    # 3. Return medical data
    return record["medical_data"]


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    try:
        data = get_patient_data("S123", "doctor", "P001")
        print("Medical Data:", data)
    except Exception as e:
        print("Error:", e)