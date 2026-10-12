from typing import Dict, Any

# Example patient records. In a real system this would be fetched from a secure database.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["metformin"]},
    },
}


def retrieve_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical data if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin', 'receptionist').
    patient_id : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        A copy of the patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to access the record.
    KeyError
        If the patient_id does not exist in PATIENT_RECORDS.
    """
    # Verify that the patient exists
    if patient_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_id}' not found.")

    record = PATIENT_RECORDS[patient_id]

    # Authorization logic:
    #   - 'admin' role can view any record
    #   - 'doctor' and 'nurse' roles must be in the assigned_staff list
    #   - all other roles are denied
    authorized = False

    if staff_role.lower() == "admin":
        authorized = True
    elif staff_role.lower() in {"doctor", "nurse"}:
        # Ensure the staff_id is part of the assigned_staff list
        authorized = staff_id in record.get("assigned_staff", [])

    if not authorized:
        raise PermissionError(
            f"Staff member '{staff_id}' with role '{staff_role}' is not authorized to access "
            f"patient '{patient_id}'."
        )

    # Return a defensive copy of the medical data to prevent accidental mutation
    return dict(record["medical_data"])


# Example usage (uncomment to test):
# try:
#     data = retrieve_patient_data("doc123", "doctor", "patient_001")
#     print(data)
# except Exception as e:
#     print(e)