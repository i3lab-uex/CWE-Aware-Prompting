# -*- coding: utf-8 -*-
"""
Patient record access module.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Example patient records database.
#
# In a real system this would be stored in a secure database and accessed
# through a well‑defined ORM or query layer.  For the purposes of this
# exercise we keep it in memory.
#
# Each record contains:
#   - patient_id: unique identifier of the patient
#   - assigned_staff: list of dictionaries, each with 'worker_id' and 'role'
#   - medical_data: dictionary containing the sensitive information
#
# --------------------------------------------------------------------------- #
PATIENT_RECORDS = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": [
            {"worker_id": "doc_a", "role": "doctor"},
            {"worker_id": "nurse_b", "role": "nurse"},
        ],
        "medical_data": {
            "diagnosis": "Hypertension",
            "treatment": "Lisinopril 10mg daily",
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": [
            {"worker_id": "doc_c", "role": "doctor"},
        ],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "treatment": "Metformin 500mg twice daily",
        },
    },
}

# --------------------------------------------------------------------------- #
# Authorization logic
#
# We enforce the following rules:
#   1. An admin may read any record.
#   2. A staff member may read a record only if they are listed in the
#      'assigned_staff' of that record.
#
# The function returns a copy of the medical data to avoid accidental
# mutation of the stored records.
#
# The implementation is deliberately simple but follows best practices:
#   - No hard‑coded role names other than 'admin'.
#   - The check is performed before any data is returned.
#   - Errors are explicit and use the built‑in PermissionError exception.
#
# --------------------------------------------------------------------------- #
def get_patient_data(worker_id: str, worker_role: str, record_id: str) -> dict:
    """
    Retrieve a patient's medical data if the requesting worker is authorized.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the healthcare professional.
    worker_role : str
        Role of the worker (e.g., 'doctor', 'nurse', 'admin').
    record_id : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        A copy of the patient's medical data.

    Raises
    ------
    PermissionError
        If the worker does not have permission to access the record.
    KeyError
        If the requested record_id is not found in PATIENT_RECORDS.
    """
    # Validate that the record exists
    if record_id not in PATIENT_RECORDS:
        raise KeyError(f"Record '{record_id}' does not exist.")

    record = PATIENT_RECORDS[record_id]

    # Admins have unrestricted access
    if worker_role.lower() == "admin":
        return record["medical_data"].copy()

    # Check if the worker is part of the assigned staff
    authorized = any(
        entry["worker_id"] == worker_id and entry["role"].lower() == worker_role.lower()
        for entry in record.get("assigned_staff", [])
    )

    if not authorized:
        raise PermissionError(
            f"Worker '{worker_id}' with role '{worker_role}' is not authorized "
            f"to access record '{record_id}'."
        )

    # Return a copy to avoid exposing internal state
    return record["medical_data"].copy()


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only; remove or comment out in production)
#
# if __name__ == "__main__":
#     try:
#         data = get_patient_data("doc_a", "doctor", "patient_001")
#         print(data)
#     except Exception as e:
#         print(e)