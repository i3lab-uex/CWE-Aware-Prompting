import datetime
from typing import Dict, Any

# Sample patient records database (in practice this would be fetched from a secure DB)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["E123", "E456"],  # employee IDs allowed to view
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Type II Diabetes"],
            "last_visit": datetime.date(2024, 6, 15),
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["E456"],
        "medical_data": {
            "name": "Jane Smith",
            "age": 30,
            "diagnosis": ["Asthma"],
            "last_visit": datetime.date(2024, 5, 20),
        },
    },
}


def retrieve_patient_data(employee_id: str, employee_role: str, patient_code: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the employee is authorized.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the healthcare professional requesting the record.
    employee_role : str
        Role of the employee (e.g., 'doctor', 'nurse', 'admin').
    patient_code : str
        Identifier of the patient whose record is being retrieved.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the employee does not have permission to access the record.
    KeyError
        If the patient_code is not found in PATIENT_RECORDS.
    """
    # Validate that the patient exists
    if patient_code not in PATIENT_RECORDS:
        raise KeyError(f"Patient with code '{patient_code}' does not exist.")

    record = PATIENT_RECORDS[patient_code]

    # Admins have blanket access
    if employee_role.lower() == "admin":
        return record["medical_data"]

    # Check if the employee is listed in assigned_staff
    if employee_id not in record["assigned_staff"]:
        raise PermissionError(
            f"Employee '{employee_id}' with role '{employee_role}' "
            "is not authorized to access this patient's data."
        )

    # Authorized: return the medical data
    return record["medical_data"]


# Example usage (uncomment to test)
# try:
#     data = retrieve_patient_data("E123", "doctor", "P001")
#     print(data)
# except Exception as e:
#     print(e)