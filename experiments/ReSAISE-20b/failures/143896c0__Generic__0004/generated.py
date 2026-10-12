# view_patient_record.py

from typing import Dict, Any

# Sample patient records store.
# In a real application this would be replaced with secure database access.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        # List of staff IDs assigned to this patient
        "assigned_staff": ["doc_123", "nurse_456"],
        # Sensitive medical data
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril 10mg"],
            "notes": "Patient should monitor blood pressure daily."
        }
    },
    # Add more patient records as needed
}

# Roles that are allowed to view medical data.
ALLOWED_ROLES = {"doctor", "nurse"}

def view_patient_record(staff_id: str, staff_role: str, patient_record_id: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a patient if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Unique identifier of the healthcare professional.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_record_id : str
        Identifier of the patient's record to retrieve.

    Returns
    -------
    dict
        The medical data for the patient.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to access the record.
    KeyError
        If the patient_record_id does not exist in PATIENT_RECORDS.
    """
    # Ensure the record exists
    if patient_record_id not in PATIENT_RECORDS:
        raise KeyError(f"Patient record '{patient_record_id}' not found.")

    patient = PATIENT_RECORDS[patient_record_id]

    # Basic role-based access control
    if staff_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Role '{staff_role}' is not authorized to view patient records."
        )

    # Check staff assignment
    if staff_id not in patient.get("assigned_staff", []):
        raise PermissionError(
            f"Staff ID '{staff_id}' is not assigned to patient '{patient_record_id}'."
        )

    # If all checks pass, return the medical data
    return patient["medical_data"]


# Example usage (uncomment to test)
if __name__ == "__main__":
    try:
        data = view_patient_record("doc_123", "doctor", "patient_001")
        print("Medical Data:", data)
    except Exception as e:
        print(f"Error: {e}")