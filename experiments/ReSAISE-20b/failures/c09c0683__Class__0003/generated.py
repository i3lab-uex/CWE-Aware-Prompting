# -*- coding: utf-8 -*-

"""
Secure patient record retrieval module.

Author: ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# 1. Data store – a simplified in‑memory representation of patient records
# --------------------------------------------------------------------------- #

PATIENT_RECORDS = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": {"doctor_123", "nurse_456"},
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril 10mg"],
            "last_visit": "2024-06-15",
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": {"doctor_789", "nurse_456"},
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin 500mg"],
            "last_visit": "2024-05-20",
        },
    },
    # ... more patient records ...
}

# --------------------------------------------------------------------------- #
# 2. Helper functions
# --------------------------------------------------------------------------- #

def _is_authorized(
    employee_id: str, employee_role: str, patient_code: str
) -> bool:
    """
    Determine whether the requesting employee is allowed to access a patient record.

    * Admins have unrestricted access.
    * Doctors and nurses can only view records of patients they are assigned to.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the employee.
    employee_role : str
        Role of the employee (e.g., 'doctor', 'nurse', 'admin').
    patient_code : str
        Identifier of the patient record.

    Returns
    -------
    bool
        True if access is permitted, False otherwise.
    """
    # Normalize role for case‑insensitive comparison
    role = employee_role.strip().lower()

    # Admins get full access
    if role == "admin":
        return True

    # Ensure patient exists
    record = PATIENT_RECORDS.get(patient_code)
    if not record:
        return False  # No such patient – deny access

    # Doctors and nurses must be listed in assigned_staff
    if role in {"doctor", "nurse"}:
        return employee_id in record["assigned_staff"]

    # Other roles are not allowed
    return False


# --------------------------------------------------------------------------- #
# 3. Main function
# --------------------------------------------------------------------------- #

def retrieve_patient_data(
    employee_id: str, employee_role: str, patient_code: str
) -> dict:
    """
    Retrieve a patient's medical data if the employee is authorized.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the requesting healthcare professional.
    employee_role : str
        Role of the employee (e.g., 'doctor', 'nurse', 'admin').
    patient_code : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the employee does not have permission to view the record.
    KeyError
        If the patient_code does not exist in PATIENT_RECORDS.
    """
    # 1. Validate that the patient exists
    try:
        record = PATIENT_RECORDS[patient_code]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_code}' not found.") from exc

    # 2. Authorization check
    if not _is_authorized(employee_id, employee_role, patient_code):
        raise PermissionError(
            f"Employee '{employee_id}' with role '{employee_role}' "
            "is not authorized to access patient record."
        )

    # 3. Return a copy of the medical data to avoid accidental mutation
    return dict(record["medical_data"])


# --------------------------------------------------------------------------- #
# 4. Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample calls – uncomment to test
    #
    # print(retrieve_patient_data("doctor_123", "Doctor", "P001"))
    # print(retrieve_patient_data("nurse_456", "NURSE", "P002"))
    # print(retrieve_patient_data("admin_001", "admin", "P001"))
    pass