from typing import Dict, Any

# Example patient records database (in practice this would be stored securely)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Roles that are allowed to read patient data
ALLOWED_ROLES = {"doctor", "nurse"}


def retrieve_patient_data(
    employee_id: str,
    employee_role: str,
    patient_code: str
) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting employee is authorized.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the healthcare professional.
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
        If the employee is not authorized to access this patient's record.
    KeyError
        If the patient_code does not exist in PATIENT_RECORDS.
    """
    # Verify that the patient exists
    if patient_code not in PATIENT_RECORDS:
        raise KeyError(f"Patient record for '{patient_code}' not found.")

    record = PATIENT_RECORDS[patient_code]

    # Authorization check
    if employee_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{employee_role}' is not authorized to access patient records."
        )

    if employee_id not in record["assigned_staff"]:
        raise PermissionError(
            f"Employee '{employee_id}' is not assigned to patient '{patient_code}'."
        )

    # Return the medical data (deep copy could be used in real systems)
    return record["medical_data"]


# Example usage (for testing purposes only):
if __name__ == "__main__":
    try:
        data = retrieve_patient_data("doc_123", "doctor", "patient_001")
        print("Medical data retrieved:", data)
    except Exception as e:
        print(f"Access denied: {e}")