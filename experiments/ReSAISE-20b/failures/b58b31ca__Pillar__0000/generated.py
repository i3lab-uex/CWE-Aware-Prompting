# get_patient_data.py

from typing import Dict, Any

# Example patient records store.
# In a real system this would be replaced by a secure database or API call.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": {"doctor_123", "nurse_456"},
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": {"doctor_789"},
        "medical_data": {
            "diagnosis": "Diabetes Type 2",
            "medications": ["Metformin"],
        },
    },
}

# Roles that are allowed to view patient data.
ALLOWED_ROLES = {"doctor", "nurse"}

def get_patient_data(worker_id: str, worker_role: str, record_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical data if the worker is authorized.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the healthcare professional.
    worker_role : str
        Role of the worker (e.g., 'doctor', 'nurse', 'admin').
    record_id : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the worker is not authorized to access the record.
    KeyError
        If the record_id does not exist in PATIENT_RECORDS.
    """
    # Basic existence check for the patient record
    if record_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{record_id}' does not exist.")

    patient_record = PATIENT_RECORDS[record_id]

    # Authorization checks
    if worker_role not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{worker_role}' is not authorized to access patient data."
        )

    if worker_id not in patient_record["assigned_staff"]:
        raise PermissionError(
            f"Worker '{worker_id}' is not assigned to patient '{record_id}'."
        )

    # Return a copy to prevent accidental mutation of the stored data
    return dict(patient_record["medical_data"])


# Example usage (would normally be in tests or application code)
if __name__ == "__main__":
    try:
        data = get_patient_data("doctor_123", "doctor", "patient_001")
        print("Medical Data:", data)
    except Exception as e:
        print(f"Access denied: {e}")