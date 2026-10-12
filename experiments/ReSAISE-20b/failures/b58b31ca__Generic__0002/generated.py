# get_patient_data.py

from typing import Dict, Any

# Example patient records store (in a real system this would be secure storage)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Define which roles are allowed to access medical data
ALLOWED_ROLES = {"doctor", "nurse"}


def get_patient_data(worker_id: str, worker_role: str, record_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical data if the requesting worker is authorized.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the healthcare professional requesting access.
    worker_role : str
        Role of the worker (e.g., 'doctor', 'nurse', 'admin').
    record_id : str
        Identifier of the patient whose record is being retrieved.

    Returns
    -------
    dict
        The medical data portion of the patient's record.

    Raises
    ------
    PermissionError
        If the worker is not authorized to view the record.
    KeyError
        If the requested patient record does not exist.
    """
    # Basic validation of input types
    if not isinstance(worker_id, str) or not isinstance(worker_role, str) or not isinstance(record_id, str):
        raise TypeError("All arguments must be strings.")

    # Check that the record exists
    try:
        patient_record = PATIENT_RECORDS[record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{record_id}' not found.") from exc

    # Verify role-based access
    if worker_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(f"Role '{worker_role}' is not permitted to access patient records.")

    # Verify staff assignment
    if worker_id not in patient_record.get("assigned_staff", []):
        raise PermissionError(f"Worker '{worker_id}' is not assigned to patient '{record_id}'.")

    # Return a copy of medical data to prevent accidental mutation
    return dict(patient_record.get("medical_data", {}))


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         data = get_patient_data("doctor_123", "doctor", "patient_001")
#         print(data)
#     except PermissionError as e:
#         print(f"Access denied: {e}")