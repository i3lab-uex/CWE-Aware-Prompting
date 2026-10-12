from typing import Dict, Any

# Example patient records database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril 10mg"],
            "notes": "Monitor blood pressure daily."
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_789"],
        "medical_data": {
            "diagnosis": "Diabetes Type 2",
            "medications": ["Metformin 500mg"],
            "notes": "Check HbA1c every 3 months."
        },
    },
}


def retrieve_patient_data(employee_id: str, employee_role: str, patient_code: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the employee is authorized.

    Args:
        employee_id: Unique identifier of the healthcare professional requesting the record.
        employee_role: Role of the employee (e.g., 'doctor', 'nurse', 'admin').
        patient_code: Identifier of the patient whose record is being retrieved.

    Returns:
        The medical_data dictionary for the specified patient.

    Raises:
        PermissionError: If the employee does not have permission to access the record.
        KeyError: If the patient_code is not found in PATIENT_RECORDS.
    """
    # Ensure the patient exists
    record = PATIENT_RECORDS[patient_code]  # Will raise KeyError if not found

    # Simple role-based access: only doctors and nurses can view medical data.
    allowed_roles = {"doctor", "nurse"}
    if employee_role.lower() not in allowed_roles:
        raise PermissionError(
            f"Role '{employee_role}' is not authorized to view patient data."
        )

    # Ensure the employee is assigned to this patient
    if employee_id not in record["assigned_staff"]:
        raise PermissionError(
            f"Employee '{employee_id}' is not assigned to patient '{patient_code}'."
        )

    # Return a copy to prevent accidental modification of the stored record
    return dict(record["medical_data"])