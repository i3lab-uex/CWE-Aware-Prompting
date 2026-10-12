# view_patient_record.py

from typing import Dict, Any


# Example patient records database.
# In a real system this would be fetched from a secure datastore.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_d1", "staff_n1"],  # IDs of staff with access
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril 10mg"],
            "notes": "Patient advised to monitor blood pressure daily."
        },
    },
    # ... more patient records
}


def _is_authorized(staff_id: str, staff_role: str, record: Dict[str, Any]) -> bool:
    """
    Internal helper that determines if a staff member is allowed to view the record.
    * Admins have blanket access.
    * Doctors and nurses can only view records where they are listed in `assigned_staff`.
    """
    # Role-based access
    if staff_role.lower() == "admin":
        return True

    # Staff must be explicitly assigned to the patient
    if staff_id in record.get("assigned_staff", []):
        return True

    # Other roles are denied
    return False


def view_patient_record(staff_id: str, staff_role: str, patient_record_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record after performing an authorization check.

    Parameters
    ----------
    staff_id : str
        Unique identifier of the requesting healthcare professional.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_record_id : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The medical data for the patient.

    Raises
    ------
    KeyError
        If the requested patient record does not exist.
    PermissionError
        If the staff member is not authorized to view the record.
    """
    # Fetch the patient record; raise KeyError if missing
    record = PATIENT_RECORDS[patient_record_id]

    # Perform the authorization check
    if not _is_authorized(staff_id, staff_role, record):
        raise PermissionError(
            f"Staff member '{staff_id}' with role '{staff_role}' is not authorized to view record "
            f"'{patient_record_id}'."
        )

    # Return a copy of the medical data to avoid accidental mutation
    return dict(record["medical_data"])


# Example usage (would normally be in a separate test or application module)
if __name__ == "__main__":
    try:
        data = view_patient_record("staff_d1", "doctor", "patient_001")
        print("Medical data retrieved:", data)
    except Exception as e:
        print("Error:", e)