import typing as _t

# --------------------------------------------------------------------------- #
# Sample data structure – in real life this would be loaded from a secure DB
# --------------------------------------------------------------------------- #
PATIENT_RECORDS: dict[str, dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Monitor blood pressure daily."
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_789"],
        "medical_data": {
            "diagnosis": "Diabetes Type 2",
            "medications": ["Metformin"],
            "notes": "Adjust diet plan."
        },
    },
}

# --------------------------------------------------------------------------- #
# Authorization logic
# --------------------------------------------------------------------------- #
def _is_authorized(
    employee_id: str,
    employee_role: str,
    patient_record: dict
) -> bool:
    """
    Determine if an employee has permission to view a patient record.

    Rules:
        * 'admin' role can read any record.
        * 'doctor' and 'nurse' roles may only read records that list their employee_id
          in the `assigned_staff` field.
        * All other roles are denied access.

    Args:
        employee_id: Unique identifier of the requesting staff member.
        employee_role: Role string (e.g., 'doctor', 'nurse', 'admin').
        patient_record: The patient record dictionary.

    Returns:
        True if authorized, False otherwise.
    """
    # Admin bypass
    if employee_role.lower() == "admin":
        return True

    # Check for doctor or nurse
    if employee_role.lower() in {"doctor", "nurse"}:
        # Ensure the record contains an assigned_staff list
        assigned = patient_record.get("assigned_staff", [])
        return employee_id in assigned

    # Default deny
    return False


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def retrieve_patient_data(
    employee_id: str,
    employee_role: str,
    patient_code: str
) -> dict:
    """
    Return the medical data for a given patient if the requesting employee is
    authorized to view it.

    Raises:
        KeyError: If `patient_code` does not exist in PATIENT_RECORDS.
        PermissionError: If the employee lacks permission to access the record.

    Args:
        employee_id: Unique identifier of the healthcare professional.
        employee_role: Role of the employee (e.g., 'doctor', 'nurse', 'admin').
        patient_code: Identifier of the patient whose record is requested.

    Returns:
        dict: The `medical_data` section of the patient's record.
    """
    # Validate existence
    if patient_code not in PATIENT_RECORDS:
        raise KeyError(f"Patient code '{patient_code}' not found.")

    record = PATIENT_RECORDS[patient_code]

    # Authorization check
    if not _is_authorized(employee_id, employee_role, record):
        raise PermissionError(
            f"Employee '{employee_id}' with role '{employee_role}' "
            "does not have permission to access patient record."
        )

    # Return a copy to prevent accidental mutation
    return dict(record.get("medical_data", {}))


# --------------------------------------------------------------------------- #
# Example usage (for testing only – remove or guard with if __name__ == "__main__")
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        data = retrieve_patient_data("doc_123", "doctor", "patient_001")
        print("Medical Data:", data)
    except Exception as e:
        print(e)