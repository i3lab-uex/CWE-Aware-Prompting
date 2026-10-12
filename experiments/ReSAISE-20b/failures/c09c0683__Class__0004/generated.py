import json
from typing import Dict, Any

# Example patient records database (normally this would be a secure datastore)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["emp_123", "emp_456"],  # IDs of authorized staff
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "last_visit": "2024-06-15",
        },
    },
    # Additional patient records...
}

def retrieve_patient_data(employee_id: str, employee_role: str, patient_code: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a specified patient if the requesting employee
    has sufficient permissions.

    Args:
        employee_id (str): Unique identifier of the requesting healthcare professional.
        employee_role (str): Role of the employee ('doctor', 'nurse', 'admin', etc.).
        patient_code (str): Identifier of the patient whose record is requested.

    Returns:
        dict: The patient's medical data.

    Raises:
        PermissionError: If the employee is not authorized to access the record.
        KeyError: If the patient_code does not exist in PATIENT_RECORDS.
    """
    # Basic validation of inputs
    if not all(isinstance(arg, str) for arg in (employee_id, employee_role, patient_code)):
        raise TypeError("All arguments must be strings")

    # Retrieve the patient record; KeyError will propagate if not found
    record = PATIENT_RECORDS[patient_code]

    # Authorization logic:
    # - Admins have blanket access
    # - Otherwise, only staff explicitly listed in 'assigned_staff' may view the record
    authorized = False
    if employee_role.lower() == "admin":
        authorized = True
    else:
        assigned_staff = record.get("assigned_staff", [])
        if employee_id in assigned_staff:
            authorized = True

    if not authorized:
        raise PermissionError(
            f"Employee '{employee_id}' with role '{employee_role}' is not authorized to access patient '{patient_code}'."
        )

    # Return a copy of the medical data to avoid accidental mutation
    return dict(record.get("medical_data", {}))