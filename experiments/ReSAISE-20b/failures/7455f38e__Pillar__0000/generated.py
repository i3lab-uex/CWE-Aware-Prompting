# get_patient_record.py

from typing import Dict, List, Any


# Example patient records database
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_a1", "nurse_b2"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Amlodipine"],
            "notes": "Monitor blood pressure daily."
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_c3"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin"],
            "notes": "Check HbA1c quarterly."
        },
    },
}


def get_patient_record(
    personnel_id: str,
    personnel_role: str,
    patient_identifier: str
) -> Dict[str, Any]:
    """
    Return the medical data for a patient if the requesting personnel has
    sufficient privileges.

    Parameters
    ----------
    personnel_id : str
        Identifier of the healthcare staff attempting to access the record.
    personnel_role : str
        Role of the requesting personnel ('doctor', 'nurse', 'admin', etc.).
    patient_identifier : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The medical data dictionary of the patient.

    Raises
    ------
    PermissionError
        If the personnel is not authorized to view the record.
    KeyError
        If the patient identifier does not exist in PATIENT_RECORDS.
    """
    # Retrieve patient record; KeyError will propagate if not found
    record = PATIENT_RECORDS[patient_identifier]

    # Define role-based access policy
    # Admins have blanket access; doctors and nurses can only view records
    # where they are listed in assigned_staff.
    if personnel_role.lower() == "admin":
        return record["medical_data"]

    if personnel_role.lower() in {"doctor", "nurse"}:
        if personnel_id in record["assigned_staff"]:
            return record["medical_data"]

    # If none of the above conditions are met, deny access
    raise PermissionError(
        f"Personnel '{personnel_id}' with role '{personnel_role}' "
        f"is not authorized to access patient '{patient_identifier}'."
    )