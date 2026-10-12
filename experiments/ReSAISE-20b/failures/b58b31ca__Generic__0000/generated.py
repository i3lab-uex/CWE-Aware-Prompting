import copy
from typing import Dict, Any

# Example patient records store (would normally be a database or secure storage)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Monitor blood pressure daily."
        },
    },
    # Additional patient records...
}

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
        A copy of the patient's medical data.

    Raises
    ------
    KeyError
        If the record_id does not exist in PATIENT_RECORDS.
    PermissionError
        If the worker is not authorized to access the record.
    """
    # Retrieve patient record; KeyError will propagate if missing
    record = PATIENT_RECORDS[record_id]

    # Basic role-based check: only doctors and nurses are allowed
    if worker_role not in {"doctor", "nurse"}:
        raise PermissionError(f"Role '{worker_role}' is not authorized to access patient records.")

    # Check that the worker is assigned to this patient
    if worker_id not in record.get("assigned_staff", []):
        raise PermissionError(f"Worker '{worker_id}' is not assigned to patient '{record_id}'.")

    # Return a deep copy of the medical data to prevent accidental mutation
    return copy.deepcopy(record["medical_data"])