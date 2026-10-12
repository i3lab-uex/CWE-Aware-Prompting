from typing import Dict, Any

# Example patient records. In a real system this would be stored in a secure database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_a", "nurse_b"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Patient advised to reduce sodium intake."
        }
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_c"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin"],
            "notes": "Monitor blood glucose daily."
        }
    },
}

def review_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Return the medical data for a patient if the staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Identifier for the healthcare personnel attempting to access the record.
    staff_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier for the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data if access is granted.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient_id is not found in PATIENT_RECORDS.
    """
    # Basic validation of inputs
    if not all(isinstance(x, str) and x for x in (staff_id, staff_role, patient_id)):
        raise ValueError("All arguments must be non‑empty strings.")

    # Retrieve the patient record; raise KeyError if missing
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_id}' not found.") from exc

    # Determine if the staff member is authorized
    is_assigned = staff_id in record.get("assigned_staff", [])
    is_admin = staff_role.lower() == "admin"

    if not (is_assigned or is_admin):
        raise PermissionError(
            f"Staff '{staff_id}' with role '{staff_role}' is not authorized "
            f"to access patient '{patient_id}'."
        )

    # Return a copy to prevent accidental modifications
    return dict(record.get("medical_data", {}))