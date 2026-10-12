from typing import Dict, Any

# Sample patient records for demonstration purposes.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_a", "nurse_b"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_c"],
        "medical_data": {
            "diagnosis": "Diabetes",
            "medications": ["Metformin"],
        },
    },
}


def get_patient_record(
    personnel_id: str,
    personnel_role: str,
    patient_identifier: str,
) -> Dict[str, Any]:
    """
    Return the medical data for a patient if access control requirements are satisfied.

    Parameters
    ----------
    personnel_id : str
        ID of the healthcare personnel requesting access.
    personnel_role : str
        Role of the personnel ('doctor', 'nurse', 'admin', etc.).
    patient_identifier : str
        ID of the patient whose record is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the personnel is not authorized to view the record.
    KeyError
        If the patient_identifier does not exist in PATIENT_RECORDS.
    """
    # Validate that the patient exists
    if patient_identifier not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_identifier}' not found.")

    record = PATIENT_RECORDS[patient_identifier]
    assigned_staff = set(record.get("assigned_staff", []))

    # Define which roles are allowed to view records
    privileged_roles = {"doctor", "nurse"}
    # Admins have full access
    if personnel_role == "admin":
        return record["medical_data"]

    # For doctors and nurses, check if they are assigned to the patient
    if personnel_role in privileged_roles:
        if personnel_id in assigned_staff:
            return record["medical_data"]

    # If none of the above conditions are met, raise a permission error
    raise PermissionError(
        f"Personnel '{personnel_id}' with role '{personnel_role}' is not authorized to access patient '{patient_identifier}'."
    )