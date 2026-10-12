# -*- coding: utf-8 -*-
"""
Patient record retrieval module.

This module defines a single public function `get_patient_data` that
allows authorised healthcare workers to retrieve the medical data for a
given patient.  The function enforces two simple security rules:

1. The worker must be listed in the patient's `assigned_staff` list.
2. The worker's role must be one of the permitted roles
   (`doctor`, `nurse`).

If either condition fails a :class:`PermissionError` is raised.

The module contains no external dependencies and can be safely imported
into a larger application.  It also includes an example `PATIENT_RECORDS`
dictionary to illustrate the expected structure.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Example data store – in a real application this would be replaced by a
# database or secure API call.
# --------------------------------------------------------------------------- #
PATIENT_RECORDS = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["worker_a", "worker_b"],
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Type II Diabetes"],
            "medications": [
                {"name": "Metformin", "dose_mg": 500},
                {"name": "Lisinopril", "dose_mg": 20}
            ],
        },
    },
    # Add more patient records as needed...
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def get_patient_data(worker_id: str, worker_role: str, record_id: str) -> dict:
    """
    Retrieve the medical data for a patient if the requesting worker is
    authorised.

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
        The patient's medical data as stored in the record.

    Raises
    ------
    KeyError
        If `record_id` is not found in :data:`PATIENT_RECORDS`.
    PermissionError
        If the worker does not have permission to view the record.
    """
    # ----------------------------------------------------------------------- #
    # 1. Retrieve patient record
    # ----------------------------------------------------------------------- #
    try:
        record = PATIENT_RECORDS[record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{record_id}' not found.") from exc

    # ----------------------------------------------------------------------- #
    # 2. Authorization checks
    # ----------------------------------------------------------------------- #
    permitted_roles = {"doctor", "nurse"}  # Extend as needed

    if worker_role.lower() not in permitted_roles:
        raise PermissionError(
            f"Role '{worker_role}' is not authorised to access patient data."
        )

    if worker_id not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Worker '{worker_id}' is not assigned to patient '{record_id}'."
        )

    # ----------------------------------------------------------------------- #
    # 3. Return the medical data
    # ----------------------------------------------------------------------- #
    return record["medical_data"]


# --------------------------------------------------------------------------- #
# Example usage (for local testing only – remove or guard with `if __name__ == "__main__":` in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        data = get_patient_data("worker_a", "doctor", "patient_001")
        print("Retrieved medical data:")
        print(data)
    except Exception as e:
        print(f"Error: {e}")