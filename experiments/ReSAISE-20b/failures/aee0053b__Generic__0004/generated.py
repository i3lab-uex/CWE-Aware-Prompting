# get_patient_data.py

from typing import Dict, Any


# Sample patient records dictionary.
# In a real application this would be replaced with secure database access.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["staff_A", "staff_B"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "treatment_plan": "Medication A, Lifestyle changes"
        }
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["staff_C"],
        "medical_data": {
            "diagnosis": "Diabetes",
            "treatment_plan": "Medication B, Monitoring"
        }
    },
    # Add more patient records as needed.
}


def get_patient_data(staff_num: str, role: str, patient_ref: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_num : str
        The ID of the healthcare professional requesting access.
    role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin', etc.).
    patient_ref : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data dictionary.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to access the requested patient record.
    KeyError
        If the patient reference does not exist in the records.

    Notes
    -----
    - The function checks that the staff member is listed in the patient's `assigned_staff`
      list. This simple rule can be extended with more complex role-based access control
      as needed.
    - The function raises `PermissionError` to clearly indicate an authorization failure,
      which is distinct from a missing patient record (`KeyError`).
    """
    # Ensure the patient exists.
    if patient_ref not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_ref}' not found.")

    patient_record = PATIENT_RECORDS[patient_ref]

    # Basic authorization check: staff must be assigned to the patient.
    if staff_num not in patient_record.get("assigned_staff", []):
        raise PermissionError(
            f"Staff member '{staff_num}' is not authorized to access patient '{patient_ref}'."
        )

    # Additional role-based checks can be inserted here if needed.
    # Example: only doctors or nurses can access medical data.
    allowed_roles = {"doctor", "nurse"}
    if role.lower() not in allowed_roles:
        raise PermissionError(
            f"Role '{role}' does not have permission to access medical data."
        )

    # If all checks pass, return the medical data.
    return patient_record["medical_data"]


# Example usage (commented out to avoid execution on import):
#
# try:
#     data = get_patient_data("staff_A", "doctor", "patient_001")
#     print(data)
# except PermissionError as e:
#     print(f"Access denied: {e}")