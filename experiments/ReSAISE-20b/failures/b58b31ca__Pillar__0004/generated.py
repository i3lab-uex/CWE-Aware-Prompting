import copy
from typing import Dict, Any

# Sample patient records. In a real system this would be stored in a secure database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["worker_a", "worker_b"],  # IDs of staff authorized to view
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Metformin"],
        },
    },
    # ... more records ...
}


def get_patient_data(worker_id: str, worker_role: str, record_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical data if the requesting worker is authorized.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the healthcare professional requesting the record.
    worker_role : str
        Role of the worker (e.g., 'doctor', 'nurse', 'admin').
    record_id : str
        Identifier of the patient whose record is being retrieved.

    Returns
    -------
    dict
        A deep copy of the patient's medical data.

    Raises
    ------
    KeyError
        If the record_id does not exist in PATIENT_RECORDS.
    PermissionError
        If the worker is not authorized to view the record.
    """

    # Retrieve the patient record; KeyError will propagate if not found
    record = PATIENT_RECORDS[record_id]

    # Basic role-based check: only 'doctor', 'nurse', or 'admin' are allowed
    if worker_role not in {"doctor", "nurse", "admin"}:
        raise PermissionError(f"Role '{worker_role}' is not authorized to access patient records.")

    # Staff assignment check: worker must be listed in assigned_staff
    if worker_id not in record.get("assigned_staff", []):
        raise PermissionError(f"Worker '{worker_id}' is not assigned to patient {record_id}.")

    # Return a deep copy to prevent accidental mutation of the stored data
    return copy.deepcopy(record["medical_data"])