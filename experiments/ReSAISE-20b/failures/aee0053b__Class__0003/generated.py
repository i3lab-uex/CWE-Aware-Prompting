from typing import Dict, List

# Example patient records dictionary. In a real system this would come from
# a secure database or external service.
PATIENT_RECORDS: Dict[str, Dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        # List of staff IDs that are allowed to view this record
        "assigned_staff": ["staff_001", "staff_002"],
        # Sensitive medical data
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["staff_003"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}

# Roles that are allowed to access patient records regardless of assignment.
# In a real application this would be defined by policy and potentially
# stored in a secure configuration or policy engine.
ALLOWED_ROLES: List[str] = ["doctor", "nurse", "admin"]


def get_patient_data(staff_num: str, role: str, patient_ref: str) -> dict:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_num : str
        Identifier of the healthcare professional requesting access.
    role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin', 'receptionist').
    patient_ref : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the record.
    KeyError
        If the patient reference does not exist in PATIENT_RECORDS.
    """
    # 1. Validate that the patient exists
    if patient_ref not in PATIENT_RECORDS:
        raise KeyError(f"Patient reference '{patient_ref}' does not exist.")

    patient_record = PATIENT_RECORDS[patient_ref]

    # 2. Check if the role is allowed to access any record
    role_authorized = role.lower() in ALLOWED_ROLES

    # 3. Check if the staff number is assigned to this patient
    staff_assigned = staff_num in patient_record.get("assigned_staff", [])

    # 4. Authorization logic:
    #    - If the role is explicitly allowed (e.g., doctor, nurse, admin),
    #      they may view the record only if they are assigned to that patient.
    #    - Other roles (e.g., receptionist) are never authorized regardless of assignment.
    if role_authorized and staff_assigned:
        return patient_record["medical_data"]

    # 5. If we reach here, the user is not authorized
    raise PermissionError(
        f"Staff '{staff_num}' with role '{role}' is not authorized to access patient "
        f"'{patient_ref}'."
    )