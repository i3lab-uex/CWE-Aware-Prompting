# get_patient_data.py

from typing import Dict, Any


# Example patient records database (in a real system this would be in a secure DB)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": {"D123", "N456"},
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": {"D123"},
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}


# Roles that are allowed to view medical data
AUTHORIZED_ROLES = {"doctor", "nurse", "admin"}


def get_patient_data(staff_num: str, role: str, patient_ref: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record for authorized staff.

    Parameters
    ----------
    staff_num : str
        Identifier of the healthcare professional requesting access.
    role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ref : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    KeyError
        If the patient record does not exist.
    PermissionError
        If the staff member is not authorized to view the patient's data.
    """
    # Validate patient existence
    if patient_ref not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_ref}' not found.")

    patient_record = PATIENT_RECORDS[patient_ref]

    # Check role-based access
    if role.lower() not in AUTHORIZED_ROLES:
        raise PermissionError(f"Role '{role}' is not authorized to access medical records.")

    # Check staff assignment
    if staff_num not in patient_record["assigned_staff"]:
        raise PermissionError(
            f"Staff member '{staff_num}' is not assigned to patient '{patient_ref}'."
        )

    # All checks passed – return medical data
    return patient_record["medical_data"]


# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     try:
#         data = get_patient_data("D123", "doctor", "P001")
#         print(data)
#     except Exception as e:
#         print(e)