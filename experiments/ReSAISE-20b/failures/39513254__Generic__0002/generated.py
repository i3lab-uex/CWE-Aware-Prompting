# Access control for patient records

# Example structure of PATIENT_RECORDS (for reference; the actual data is expected to be provided elsewhere)
# PATIENT_RECORDS = {
#     "patient_001": {
#         "patient_id": "patient_001",
#         "assigned_staff": {"doctor:dr_smith", "nurse:nurse_amy"},
#         "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
#     },
#     # ... more patient records ...
# }

def access_patient_record(user_id: str, user_role: str, patient_id: str):
    """
    Retrieve a patient's medical data if the requesting user is authorized.

    Parameters
    ----------
    user_id : str
        Identifier of the healthcare professional attempting access.
    user_role : str
        Role of the user (e.g., 'doctor', 'nurse', 'admin', 'receptionist').
    patient_id : str
        Identifier of the patient whose record is being accessed.

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
    # Basic validation of input types
    if not isinstance(user_id, str) or not isinstance(user_role, str) or not isinstance(patient_id, str):
        raise TypeError("user_id, user_role, and patient_id must be strings")

    # Ensure the patient record exists
    if patient_id not in PATIENT_RECORDS:
        raise ValueError(f"Patient record '{patient_id}' does not exist")

    record = PATIENT_RECORDS[patient_id]
    assigned_staff = set(record.get("assigned_staff", []))

    # Define role-based permissions
    allowed_roles = {"doctor", "nurse", "admin"}
    if user_role not in allowed_roles:
        raise PermissionError(f"Role '{user_role}' is not permitted to access patient records")

    # Admins can view any record
    if user_role == "admin":
        return record["medical_data"]

    # For doctors and nurses, check if they are assigned to the patient
    role_prefix = f"{user_role}:{user_id}"
    if role_prefix in assigned_staff:
        return record["medical_data"]

    # If none of the conditions are met, deny access
    raise PermissionError("User is not authorized to access this patient's record")