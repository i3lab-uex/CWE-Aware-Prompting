# -*- coding: utf-8 -*-
"""
Secure patient record retrieval module.

Author: OpenAI ChatGPT
"""

from typing import Dict, List

# Example patient records database. In a real system this would be fetched from
# a secure database rather than being hard‑coded.
PATIENT_RECORDS: Dict[str, Dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc123", "nurse456"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "treatment_plan": ["Medication A", "Lifestyle changes"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc789"],
        "medical_data": {
            "diagnosis": "Diabetes",
            "treatment_plan": ["Medication B", "Insulin therapy"],
        },
    },
}

# Roles that are allowed to view medical data. In practice, this list would
# be configurable and stored in a secure configuration store.
ALLOWED_ROLES: List[str] = ["doctor", "nurse"]


def fetch_patient_record(
    staff_identifier: str, staff_role: str, patient_ident: str
) -> Dict:
    """
    Retrieve a patient's medical record if the requesting staff member is authorized.

    Parameters
    ----------
    staff_identifier : str
        The unique identifier of the healthcare professional making the request.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_ident : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to access the patient's record.
    KeyError
        If the patient identifier does not exist in the records database.

    Notes
    -----
    The function first checks that the role is permitted to view records, then verifies
    that the staff member is listed in the patient's assigned_staff.  This two‑step
    check mitigates CWE‑863 (Incorrect Authorization) by ensuring that both role and
    assignment are validated before data is returned.
    """
    # Validate existence of patient record
    if patient_ident not in PATIENT_RECORDS:
        raise KeyError(f"Patient ID '{patient_ident}' not found.")

    record = PATIENT_RECORDS[patient_ident]

    # Role-based check
    if staff_role.lower() not in ALLOWED_ROLES:
        raise PermissionError(
            f"Access denied: role '{staff_role}' is not authorized to view patient records."
        )

    # Assignment check
    if staff_identifier not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Access denied: staff '{staff_identifier}' is not assigned to patient '{patient_ident}'."
        )

    # All checks passed; return medical data
    return record["medical_data"]