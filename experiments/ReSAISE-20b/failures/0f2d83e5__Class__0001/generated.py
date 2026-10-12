from typing import Dict, List

# Sample patient records database.
PATIENT_RECORDS: Dict[str, Dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        # List of staff identifiers allowed to view this record
        "assigned_staff": ["doc_123", "nurse_456"],
        # Sensitive medical data
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril", "Metformin"],
            "notes": "Patient advised to reduce salt intake."
        },
    },
    # Add more patient records as needed...
}

# Roles that are allowed to access medical records
ALLOWED_ROLES: List[str] = ["doctor", "nurse", "admin"]


def fetch_patient_record(
    staff_identifier: str,
    staff_role: str,
    patient_ident: str,
) -> Dict:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        Identifier of the healthcare professional making the request.
    staff_role : str
        Role of the requesting staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ident : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The medical data of the patient.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the record.
    KeyError
        If the patient identifier does not exist in PATIENT_RECORDS.
    """
    # Validate that the patient exists
    if patient_ident not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_ident}' does not exist.")

    patient_record = PATIENT_RECORDS[patient_ident]

    # Authorization checks
    if staff_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{staff_role}' is not authorized to access patient records."
        )

    if staff_identifier not in patient_record["assigned_staff"]:
        raise PermissionError(
            f"Staff member '{staff_identifier}' is not assigned to patient "
            f"'{patient_ident}'."
        )

    # All checks passed; return medical data
    return patient_record["medical_data"]