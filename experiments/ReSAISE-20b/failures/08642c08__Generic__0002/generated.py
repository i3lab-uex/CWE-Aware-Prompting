# -*- coding: utf-8 -*-

from typing import Dict, Any

# Example patient records dictionary
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
    # Add more patient records as needed
}


def fetch_patient_info(staff_identifier: str, staff_role: str, patient_ref: str) -> Any:
    """
    Retrieve the medical data for a given patient if access control checks pass.

    Parameters
    ----------
    staff_identifier : str
        Identifier of the healthcare personnel requesting access.
    staff_role : str
        Role of the requester (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        Identifier of the patient whose data is requested.

    Returns
    -------
    Any
        The patient's medical data if access is authorized.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to access the record.
    KeyError
        If the patient_ref is not found in PATIENT_RECORDS.
    """
    # Validate that the patient exists
    if patient_ref not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_ref}' does not exist.")

    patient_record = PATIENT_RECORDS[patient_ref]

    # Admins bypass all checks
    if staff_role.lower() == "admin":
        return patient_record["medical_data"]

    # For non-admins, ensure staff is explicitly assigned to this patient
    if staff_identifier not in patient_record.get("assigned_staff", []):
        raise PermissionError(
            f"Unauthorized access: staff '{staff_identifier}' "
            f"does not have permission to view patient '{patient_ref}'."
        )

    # Access granted
    return patient_record["medical_data"]


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         data = fetch_patient_info("doctor_a", "doctor", "patient_001")
#         print(data)
#     except Exception as e:
#         print(e)