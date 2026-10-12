# get_patient_data.py

from typing import Dict, Any

# Example patient records dictionary.
# In a real system this would be loaded from a secure database or encrypted store.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["worker_a", "worker_b"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["worker_c"],
        "medical_data": {
            "diagnosis": "Diabetes",
            "medications": ["Metformin"],
        },
    },
    # Additional records...
}

# Roles that are allowed to read patient data
ALLOWED_ROLES = {"doctor", "nurse"}

def get_patient_data(worker_id: str, worker_role: str, record_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical data if the requesting worker is authorized.

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
        The medical data portion of the patient's record.

    Raises
    ------
    PermissionError
        If the worker is not authorized to access the requested record.
    KeyError
        If the requested patient record does not exist.
    """
    # Verify that the record exists
    try:
        record = PATIENT_RECORDS[record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{record_id}' not found.") from exc

    # Authorization: role must be allowed
    if worker_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{worker_role}' is not authorized to access patient records."
        )

    # Authorization: worker must be assigned to the patient
    if worker_id not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Worker '{worker_id}' is not assigned to patient '{record_id}'."
        )

    # All checks passed; return medical data
    return record.get("medical_data", {})

# Example usage (commented out to avoid execution on import)
# if __name__ == "__main__":
#     try:
#         data = get_patient_data("worker_a", "doctor", "patient_001")
#         print(data)
#     except Exception as e:
#         print(e)