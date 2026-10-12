from __future__ import annotations

# Example patient records structure.
# In a real application this would be loaded from a secure database.
PATIENT_RECORDS = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril 10mg"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc789"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin 500mg"],
        },
    },
}


def get_patient_record(
    personnel_id: str,
    personnel_role: str,
    patient_identifier: str,
) -> dict:
    """
    Return the medical data for a patient if the calling personnel has permission.

    Parameters
    ----------
    personnel_id : str
        Identifier of the healthcare staff attempting access.
    personnel_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_identifier : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The medical data associated with the patient.

    Raises
    ------
    PermissionError
        If the personnel is not authorized to view the record.
    KeyError
        If the patient_identifier does not exist in PATIENT_RECORDS.
    """
    # Validate that the patient exists
    if patient_identifier not in PATIENT_RECORDS:
        raise KeyError(f"Patient '{patient_identifier}' not found.")

    record = PATIENT_RECORDS[patient_identifier]

    # Authorization logic
    authorized = False

    # Admins can view any record
    if personnel_role.lower() == "admin":
        authorized = True

    # Staff assigned to the patient can view
    elif personnel_id in record.get("assigned_staff", []):
        authorized = True

    # If not authorized, raise PermissionError
    if not authorized:
        raise PermissionError(
            f"Personnel '{personnel_id}' with role '{personnel_role}' "
            "is not authorized to access this patient record."
        )

    # Return a copy to prevent accidental mutation of the stored data
    return dict(record["medical_data"])