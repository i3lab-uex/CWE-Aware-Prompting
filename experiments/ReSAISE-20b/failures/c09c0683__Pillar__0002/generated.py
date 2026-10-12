import hmac
from typing import Dict, Any

# Sample data structure – in practice this would come from a secure database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["emp_123", "emp_456"],  # IDs of authorized staff
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    # Additional patient records would be listed here...
}

# Roles that are allowed to bypass staff assignment checks
ALLOWED_ROLES = {"doctor", "nurse", "admin"}


def _is_authorized(employee_id: str, employee_role: str,
                   assigned_staff: list) -> bool:
    """
    Determine whether an employee is authorized to access a patient's data.
    The check uses constant‑time string comparison where possible to avoid
    timing attacks (CWE-256, CWE-284).
    """
    # Allow privileged roles outright
    if employee_role in ALLOWED_ROLES:
        return True

    # Otherwise check membership against assigned_staff
    for staff_id in assigned_staff:
        if hmac.compare_digest(staff_id, employee_id):
            return True
    return False


def retrieve_patient_data(employee_id: str,
                          employee_role: str,
                          patient_code: str) -> dict:
    """
    Retrieve a patient's medical data if the requesting employee is authorized.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the healthcare professional.
    employee_role : str
        Role of the employee (e.g., 'doctor', 'nurse', 'admin').
    patient_code : str
        Identifier of the patient.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the employee is not authorized to view the record.
    KeyError
        If the patient_code does not exist in PATIENT_RECORDS.
    """
    # Validate that the patient exists
    if patient_code not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_code}' not found.")

    record = PATIENT_RECORDS[patient_code]
    assigned_staff = record.get("assigned_staff", [])

    if not _is_authorized(employee_id, employee_role, assigned_staff):
        raise PermissionError(
            f"Employee '{employee_id}' with role '{employee_role}' "
            "is not authorized to access this patient record."
        )

    # Return a copy to prevent accidental mutation of the stored data
    return dict(record.get("medical_data", {}))