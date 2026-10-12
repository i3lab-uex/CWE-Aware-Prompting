# -*- coding: utf-8 -*-
"""
Access control for patient records.

The function `access_patient_record` enforces the following rules:

* A **doctor** or **nurse** can only view records of patients for whom they are listed
  in the patient's `assigned_staff` list.
* An **admin** can view any patient record.
* A **receptionist** (or any other role) is not allowed to view medical data.
* If the patient record does not exist, a `ValueError` is raised.
* If access is denied due to insufficient privileges, a `PermissionError`
  is raised.

The implementation guards against CWE-284 (Improper Access Control) by
explicitly checking user roles and ensuring that staff membership is verified.
"""

from typing import Dict, Any

# Example patient records store
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doctor_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medication": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doctor_789"],
        "medical_data": {"diagnosis": "Diabetes", "medication": ["Metformin"]},
    },
    # Add more patient records as needed
}


def access_patient_record(user_id: str, user_role: str, patient_id: str) -> Dict[str, Any]:
    """
    Retrieve a patient's medical data if the requesting user is authorized.

    Parameters
    ----------
    user_id : str
        Identifier of the healthcare professional requesting access.
    user_role : str
        Role of the user: 'doctor', 'nurse', 'admin', or others.
    patient_id : str
        Identifier of the patient whose record is requested.

    Returns
    -------
    dict
        The medical data dictionary of the patient.

    Raises
    ------
    ValueError
        If no record exists for the given `patient_id`.
    PermissionError
        If the user is not authorized to access the record.
    """
    # 1. Validate that the patient record exists
    record = PATIENT_RECORDS.get(patient_id)
    if record is None:
        raise ValueError(f"Patient record with ID '{patient_id}' does not exist.")

    # 2. Determine authorization based on role
    if user_role == "admin":
        # Admins have blanket access
        return record["medical_data"]

    if user_role in ("doctor", "nurse"):
        # Doctors and nurses must be explicitly assigned to the patient
        if user_id in record.get("assigned_staff", []):
            return record["medical_data"]
        else:
            raise PermissionError(
                f"Access denied: {user_role} '{user_id}' is not assigned to patient '{patient_id}'."
            )

    # 3. All other roles (e.g., receptionist) are denied
    raise PermissionError(
        f"Access denied: role '{user_role}' is not authorized to view medical records."
    )