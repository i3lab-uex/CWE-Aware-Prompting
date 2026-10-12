from typing import Dict, Any

# Sample patient records database (in practice this would be fetched from a secure datastore)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_a123", "nurse_b456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_c789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}


def get_patient_record(personnel_id: str, personnel_role: str, patient_identifier: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a given patient if the requesting personnel is authorized.

    Args:
        personnel_id (str): ID of the healthcare staff attempting access.
        personnel_role (str): Role of the requesting staff member ('doctor', 'nurse', 'admin', etc.).
        patient_identifier (str): ID of the patient whose record is requested.

    Returns:
        dict: The medical data dictionary for the patient.

    Raises:
        PermissionError: If the personnel is not authorized to view the patient's record.
        KeyError: If the patient_identifier does not exist in PATIENT_RECORDS.
    """
    # 1. Ensure the patient exists
    if patient_identifier not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_identifier}' does not exist.")

    record = PATIENT_RECORDS[patient_identifier]

    # 2. Authorization logic
    #   a) Admins have full access.
    #   b) Doctors and nurses can only view records of patients to whom they are assigned.
    #   c) Any other roles are denied.
    authorized = False
    if personnel_role.lower() == "admin":
        authorized = True
    elif personnel_role.lower() in {"doctor", "nurse"}:
        # Use a set for efficient lookup
        authorized = personnel_id in set(record.get("assigned_staff", []))

    # 3. If not authorized, raise PermissionError
    if not authorized:
        raise PermissionError(
            f"Personnel '{personnel_id}' with role '{personnel_role}' is not authorized to access "
            f"patient '{patient_identifier}'."
        )

    # 4. Return the medical data
    return record["medical_data"]