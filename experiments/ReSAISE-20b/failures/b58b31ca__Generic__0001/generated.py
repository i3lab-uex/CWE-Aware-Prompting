from __future__ import annotations

import json
from typing import Any, Dict, List

# Sample data structure. In real life this would be fetched from a secure DB.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
            "notes": "Patient advised to reduce salt intake."
        },
    },
    # ... more records
}

# Define which roles are always granted access (e.g., administrators)
ALLOWED_ROLES: List[str] = ["admin", "supervisor"]


def get_patient_data(worker_id: str, worker_role: str, record_id: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a patient record if the requesting worker is authorized.

    Args:
        worker_id (str): Unique identifier of the healthcare professional.
        worker_role (str): Role of the worker (e.g., 'doctor', 'nurse', 'admin').
        record_id (str): Identifier of the patient record to retrieve.

    Returns:
        dict: The patient's medical data.

    Raises:
        PermissionError: If the worker does not have permission to access the record.
        KeyError: If the requested record_id is not found in PATIENT_RECORDS.
    """
    # Check if the record exists
    try:
        record = PATIENT_RECORDS[record_id]
    except KeyError as exc:
        raise KeyError(f"Record '{record_id}' not found.") from exc

    # Authorization logic
    if worker_role.lower() in (role.lower() for role in ALLOWED_ROLES):
        # Admins and supervisors have blanket access
        authorized = True
    else:
        # Otherwise, check if the worker is explicitly assigned to this patient
        authorized = worker_id in record.get("assigned_staff", [])

    if not authorized:
        raise PermissionError(
            f"Worker '{worker_id}' with role '{worker_role}' is not authorized to access record '{record_id}'."
        )

    # Return a copy to prevent accidental modifications
    return json.loads(json.dumps(record.get("medical_data", {})))


# Example usage (would normally be in a separate test or application file)
if __name__ == "__main__":
    try:
        data = get_patient_data("doc123", "doctor", "patient_001")
        print("Medical Data:", data)
    except Exception as e:
        print(f"Error: {e}")