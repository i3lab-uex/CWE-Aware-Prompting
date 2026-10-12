# -*- coding: utf-8 -*-
"""
Module providing secure patient data access for healthcare staff.
"""

from __future__ import annotations
from typing import Dict, Any, List

# Sample patient records database.
# In a real application this would be replaced with a secure persistent store.
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["S1001", "S2002"],  # staff IDs allowed to view
        "medical_data": {
            "diagnosis": "Hypertension",
            "treatment_plan": ["Medication A", "Lifestyle changes"],
        },
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["S3003"],
        "medical_data": {
            "diagnosis": "Diabetes",
            "treatment_plan": ["Medication B", "Dietary plan"],
        },
    },
}


def review_patient_data(staff_id: str, staff_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Return the medical data for a patient if access is authorized.

    Parameters
    ----------
    staff_id : str
        The ID of the healthcare personnel attempting access.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        The ID of the patient whose data is requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    PermissionError
        If the staff member is not authorized to view the record.
    KeyError
        If the patient_id does not exist in PATIENT_RECORDS.
    """
    # Validate input types (basic defensive programming)
    if not isinstance(staff_id, str) or not isinstance(staff_role, str) or not isinstance(patient_id, str):
        raise TypeError("staff_id, staff_role and patient_id must be strings")

    # Retrieve the patient's record
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_id}' not found") from exc

    # Authorization logic:
    # 1. Admins can access any record.
    # 2. Otherwise, the staff_id must be listed in assigned_staff.
    if staff_role.lower() == "admin":
        authorized = True
    else:
        # Ensure exact match; use a set for efficient lookup.
        authorized = staff_id in set(record.get("assigned_staff", []))

    if not authorized:
        raise PermissionError(
            f"Access denied for staff ID '{staff_id}' with role '{staff_role}' "
            f"to patient record '{patient_id}'."
        )

    # Return a copy to prevent accidental mutation of the stored data.
    return dict(record.get("medical_data", {}))