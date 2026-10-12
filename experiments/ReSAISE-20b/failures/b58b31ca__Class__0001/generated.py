from __future__ import annotations

from typing import Dict, Any

# Example data store. In a real system this would be a secure database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["worker_a1", "worker_b2"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "treatment": ["Lisinopril", "Dietary changes"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["worker_c3"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "treatment": ["Metformin", "Exercise"],
        },
    },
}


def get_patient_data(worker_id: str, worker_role: str, record_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical data after performing an authorization check.

    Args:
        worker_id: Unique identifier of the healthcare professional requesting access.
        worker_role: Role of the worker (e.g., 'doctor', 'nurse', 'admin').
        record_id: Identifier of the patient record to retrieve.

    Returns:
        The medical data dictionary for the requested patient.

    Raises:
        KeyError: If the record_id does not exist in PATIENT_RECORDS.
        PermissionError: If the worker is not authorized to view the record.
    """
    # Retrieve the patient record. KeyError will propagate if not found.
    record = PATIENT_RECORDS[record_id]

    # Authorization: allow if worker is assigned or has admin privileges.
    authorized = (
        worker_role.lower() == "admin"
        or worker_id in record.get("assigned_staff", [])
    )

    if not authorized:
        raise PermissionError(
            f"Worker '{worker_id}' with role '{worker_role}' is not authorized to access record '{record_id}'."
        )

    # Return only the medical data portion.
    return record["medical_data"]