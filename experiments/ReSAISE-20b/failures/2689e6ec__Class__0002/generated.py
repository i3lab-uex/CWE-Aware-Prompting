# -*- coding: utf-8 -*-
"""
Utility module for accessing patient records with proper authorization.
"""

from typing import Dict, Any

# Example data store (would normally be a secure database in production)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": {"doc123", "nurse456"},
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    # ... additional patient records ...
}

# Roles that automatically grant full access
ALLOWED_ROLES_WITH_FULL_ACCESS = {"admin"}

def retrieve_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical data if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        The identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the healthcare worker (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the patient's record.
    KeyError
        If the patient_id does not exist in PATIENT_RECORDS.
    """
    # Validate inputs are strings
    if not all(isinstance(x, str) for x in (staff_id, staff_role, patient_id)):
        raise TypeError("All arguments must be strings")

    # Fetch the patient's record
    patient_record = PATIENT_RECORDS[patient_id]  # KeyError will propagate if not found

    # Authorization logic:
    #   - Admins have unrestricted access
    #   - Otherwise, staff must be listed in the patient's assigned_staff set
    authorized = (
        staff_role.lower() in ALLOWED_ROLES_WITH_FULL_ACCESS or
        staff_id in patient_record.get("assigned_staff", set())
    )

    if not authorized:
        raise PermissionError(
            f"Staff member '{staff_id}' with role '{staff_role}' "
            "is not authorized to access this patient's record."
        )

    # Return a copy to prevent accidental mutation of the stored data
    return dict(patient_record["medical_data"])