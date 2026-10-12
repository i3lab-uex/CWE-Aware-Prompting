# -*- coding: utf-8 -*-
"""
A small module that demonstrates controlled access to patient records.
"""

from typing import Dict, Any

# Example data store (in a real system this would be in a secure database)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": {"doctor": ["doc_a"], "nurse": ["nurse_b"]},
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
            "notes": "Patient advised to monitor blood pressure daily."
        },
    },
    # Add more patient records as needed
}


def get_patient_data(worker_id: str, worker_role: str, record_id: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a patient if the requesting worker is authorized.

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
        The medical data for the specified patient.

    Raises
    ------
    PermissionError
        If the worker does not have permission to access the record.
    KeyError
        If the requested patient record does not exist.
    """
    # Validate input types (basic sanity check)
    if not all(isinstance(arg, str) for arg in (worker_id, worker_role, record_id)):
        raise TypeError("All arguments must be strings.")

    # Retrieve the patient record
    try:
        record = PATIENT_RECORDS[record_id]
    except KeyError as exc:
        raise KeyError(f"Patient record '{record_id}' not found.") from exc

    # Check if the worker is assigned to this role for this patient
    allowed_workers = record.get("assigned_staff", {}).get(worker_role, [])
    if worker_id not in allowed_workers:
        # For security reasons we do NOT reveal whether the record exists
        raise PermissionError("You do not have permission to access this patient data.")

    # Return a copy of the medical data to avoid accidental modifications
    return dict(record["medical_data"])


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    try:
        data = get_patient_data("doc_a", "doctor", "patient_001")
        print("Medical Data:", data)
    except PermissionError as pe:
        print("Access denied:", pe)
    except Exception as e:
        print("Error:", e)