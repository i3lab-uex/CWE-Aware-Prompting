import json
from typing import Dict, Any

# Example patient records store. In a real system this would be
# backed by a secure database or encrypted file.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["E123", "E456"],  # employee IDs
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Type 2 Diabetes"],
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["E789"],
        "medical_data": {
            "name": "Jane Smith",
            "age": 30,
            "diagnosis": ["Asthma"],
        },
    },
}

def retrieve_patient_data(
    employee_id: str,
    employee_role: str,
    patient_code: str
) -> Dict[str, Any]:
    """
    Retrieve the medical data of a patient if the requesting employee
    is authorized.

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
        The medical data for the specified patient.

    Raises
    ------
    KeyError
        If the `patient_code` does not exist in PATIENT_RECORDS.
    PermissionError
        If the employee is not authorized to view the patient's record.
    """
    # Validate patient exists
    if patient_code not in PATIENT_RECORDS:
        raise KeyError(f"Patient with code '{patient_code}' not found.")

    record = PATIENT_RECORDS[patient_code]

    # Admins have blanket access
    if employee_role.lower() == "admin":
        return record["medical_data"]

    # Check if the employee is part of the assigned staff
    if employee_id in record.get("assigned_staff", []):
        return record["medical_data"]

    # If neither condition is met, raise a PermissionError
    raise PermissionError(
        f"Employee '{employee_id}' (role: {employee_role}) "
        f"is not authorized to access patient '{patient_code}'."
    )

# Example usage (for testing purposes only; remove or guard with if __name__ == "__main__")
if __name__ == "__main__":
    try:
        data = retrieve_patient_data("E123", "doctor", "P001")
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")