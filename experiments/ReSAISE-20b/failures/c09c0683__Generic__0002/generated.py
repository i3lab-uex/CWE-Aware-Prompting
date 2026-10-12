from typing import Dict, Any

# Example patient records database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["E123", "E456"],  # employee IDs
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["E789"],
        "medical_data": {
            "diagnosis": "Diabetes",
            "medications": ["Metformin"],
        },
    },
}


def retrieve_patient_data(employee_id: str, employee_role: str, patient_code: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting employee is authorized.

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
        If the employee is not authorized to access the record.
    KeyError
        If the patient_code does not exist in PATIENT_RECORDS.
    """
    # Ensure the patient exists
    if patient_code not in PATIENT_RECORDS:
        raise KeyError(f"Patient code '{patient_code}' not found.")

    record = PATIENT_RECORDS[patient_code]

    # Authorization logic
    is_assigned_staff = employee_id in record.get("assigned_staff", [])
    is_doctor = employee_role.lower() == "doctor"

    if not (is_assigned_staff or is_doctor):
        raise PermissionError(
            f"Employee '{employee_id}' with role '{employee_role}' "
            "does not have permission to access this patient's data."
        )

    # Return a copy to prevent accidental modifications
    return dict(record.get("medical_data", {}))