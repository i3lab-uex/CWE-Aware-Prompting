from typing import Dict, List

# Sample patient records database
PATIENT_RECORDS: Dict[str, Dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_789", "nurse_456"],
        "medical_data": {
            "name": "Jane Smith",
            "age": 32,
            "diagnosis": "Asthma",
            "medications": ["Albuterol"],
        },
    },
}


def get_patient_data(
    worker_id: str, worker_role: str, record_id: str
) -> Dict:
    """
    Retrieve a patient's medical data if the requesting worker is authorized.

    Args:
        worker_id (str): Unique identifier of the healthcare professional.
        worker_role (str): Role of the worker (e.g., 'doctor', 'nurse', 'admin').
        record_id (str): Identifier of the patient whose record is requested.

    Returns:
        dict: The medical data for the specified patient.

    Raises:
        PermissionError: If the worker does not have permission to access the record.
        KeyError: If the patient record does not exist.
    """
    # Verify that the requested record exists
    if record_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{record_id}' does not exist.")

    record = PATIENT_RECORDS[record_id]

    # Only doctors and nurses may access patient data
    if worker_role not in {"doctor", "nurse"}:
        raise PermissionError(
            f"Role '{worker_role}' is not authorized to access patient data."
        )

    # Ensure the worker is assigned to this patient
    if worker_id not in record["assigned_staff"]:
        raise PermissionError(
            f"Worker '{worker_id}' is not assigned to patient '{record_id}'."
        )

    # Return a copy of the medical data to avoid accidental mutation
    return dict(record["medical_data"])


# Example usage (uncomment to test)
# try:
#     data = get_patient_data("doctor_123", "doctor", "patient_001")
#     print(data)
# except Exception as e:
#     print(e)