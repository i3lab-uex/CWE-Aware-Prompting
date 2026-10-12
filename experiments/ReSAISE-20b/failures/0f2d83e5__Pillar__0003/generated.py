# -*- coding: utf-8 -*-

"""
Healthcare patient record access module.

This module provides a secure interface for retrieving medical records
while enforcing proper authorization checks to prevent CWE-284
(Improper Access Control) vulnerabilities.
"""

from typing import Dict, Any

# Sample patient records database (in a real system this would be
# replaced by a secure persistent store such as a database).
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": {"doctor:dr_smith", "nurse:nurse_jane"},
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    # Additional patient entries would follow the same structure.
}

# Custom exception for unauthorized access attempts
class aPermissionError(PermissionError):
    """Raised when an attempt is made to access a patient record without
    proper authorization."""
    pass


def fetch_patient_record(staff_identifier: str, staff_role: str, patient_ident: str) -> Dict[str, Any]:
    """
    Retrieve the medical data for a specified patient if the requesting
    staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        The unique identifier of the healthcare professional requesting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin',
        'receptionist'). Roles are case‑insensitive.
    patient_ident : str
        The unique identifier of the patient whose record is being accessed.

    Returns
    -------
    dict
        The medical data of the patient.

    Raises
    ------
    aPermissionError
        If the staff member does not have permission to view the record.
    KeyError
        If the patient identifier is not found in the database.

    Notes
    -----
    - Only staff members whose identifiers are listed in a patient's
      ``assigned_staff`` set, or who hold an ``admin`` role,
      are permitted to access the record.
    - Role names are compared in a case‑insensitive manner to avoid
      privilege escalation via case differences.
    - The function performs a strict membership check rather than relying on
      any implicit trust, mitigating the risk of improper access control.
    """
    # Normalise inputs
    staff_role_clean = staff_role.strip().lower()
    patient_id_clean = patient_ident.strip()

    # Verify the patient exists
    if patient_id_clean not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_id_clean}' not found.")

    record = PATIENT_RECORDS[patient_id_clean]

    # Admins have blanket access
    if staff_role_clean == "admin":
        return record["medical_data"]

    # Build the expected identifier string for membership checks
    staff_token = f"{staff_role_clean}:{staff_identifier.strip()}"

    # Check if the staff member is assigned to this patient
    if staff_token in record["assigned_staff"]:
        return record["medical_data"]

    # If we reach this point, access is denied
    raise aPermissionError(
        f"Unauthorized access attempt by {staff_role_clean} "
        f"'{staff_identifier}' for patient '{patient_id_clean}'."
    )