import json
from typing import Dict, Any

# Example patient records store.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_a", "nurse_b"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_c"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}


def access_patient_record(user_id: str, user_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Return the medical data for a given patient if the user is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the healthcare professional attempting to access the record.
    user_role : str
        The role of the user (e.g., 'doctor', 'nurse', 'admin', or 'receptionist').
    patient_id : str
        The ID of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    ValueError
        If the patient record does not exist.
    PermissionError
        If the user is not authorized to access the record.
    """
    # 1. Check that the patient exists
    if patient_id not in PATIENT_RECORDS:
        raise ValueError(f"Patient record for ID '{patient_id}' does not exist.")

    patient_record = PATIENT_RECORDS[patient_id]

    # 2. Authorization logic
    if user_role.lower() == "admin":
        # Admins have full access to all records
        authorized = True
    elif user_role.lower() in {"doctor", "nurse"}:
        # Doctors and nurses must be explicitly assigned to the patient
        authorized = user_id in patient_record.get("assigned_staff", [])
    else:
        # Other roles (e.g., receptionist) are not allowed to view medical data
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized to access patient '{patient_id}'."
        )

    # 3. Return the medical data (deep copy to avoid accidental mutation)
    return json.loads(json.dumps(patient_record.get("medical_data", {})))