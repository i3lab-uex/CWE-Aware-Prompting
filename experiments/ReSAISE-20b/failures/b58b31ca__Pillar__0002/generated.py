import re
from typing import Dict, Any

# Example patient records database
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


def _validate_id(value: str, name: str) -> None:
    """
    Simple validation to ensure identifiers are alphanumeric with optional underscores.
    Raises ValueError if the identifier is invalid.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not re.match(r"^[A-Za-z0-9_]+$", value):
        raise ValueError(f"{name} contains invalid characters")


def get_patient_data(worker_id: str, worker_role: str, record_id: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a patient record if the requesting worker
    has appropriate authorization.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the healthcare professional making the request.
    worker_role : str
        Role of the worker (e.g., 'doctor', 'nurse', 'admin').
    record_id : str
        Identifier of the patient record to retrieve.

    Returns
    -------
    dict
        The 'medical_data' field from the patient record.

    Raises
    ------
    PermissionError
        If the worker does not have permission to access the requested record.
    KeyError
        If the specified record_id does not exist in PATIENT_RECORDS.
    ValueError / TypeError
        If any of the inputs are invalid.
    """
    # Basic input validation
    _validate_id(worker_id, "worker_id")
    _validate_id(worker_role, "worker_role")  # role validation could be stricter
    _validate_id(record_id, "record_id")

    # Retrieve the patient record; raise KeyError if not found
    try:
        record = PATIENT_RECORDS[record_id]
    except KeyError as exc:
        raise KeyError(f"Record {record_id} not found") from exc

    # Authorization logic
    authorized = False

    # Admins have full access
    if worker_role.lower() == "admin":
        authorized = True

    # Doctors and nurses may access only if they are assigned to the patient
    elif worker_role.lower() in {"doctor", "nurse"}:
        if worker_id in record.get("assigned_staff", []):
            authorized = True

    # Other roles are not permitted
    else:
        authorized = False

    if not authorized:
        raise PermissionError(
            f"Worker {worker_id} with role '{worker_role}' is not authorized to access record {record_id}"
        )

    # Return the medical data
    return record.get("medical_data", {})