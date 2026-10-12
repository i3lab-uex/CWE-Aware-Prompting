# -*- coding: utf-8 -*-
"""
Medical data access module

Author: OpenAI
"""

from __future__ import annotations

# Example patient records dictionary
PATIENT_RECORDS = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_a1", "nurse_b2"],
        "medical_data": {
            "name": "John Doe",
            "age": 45,
            "diagnosis": ["Hypertension", "Diabetes"],
            "medications": ["Metformin", "Lisinopril"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_c3"],
        "medical_data": {
            "name": "Jane Smith",
            "age": 32,
            "diagnosis": ["Asthma"],
            "medications": ["Albuterol"],
        },
    },
}

# Allowed roles that can view patient data
ALLOWED_ROLES = {"doctor", "nurse", "admin"}


def review_patient_data(staff_id: str, staff_role: str, patient_id: str):
    """
    Return medical data for a patient if access control checks pass.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare personnel requesting access.
    staff_role : str
        Role of the requester (e.g., 'doctor', 'nurse', 'admin').
    patient_id : str
        Identifier of the patient whose data is requested.

    Returns
    -------
    dict
        The medical data dictionary for the patient.

    Raises
    ------
    PermissionError
        If the requester is not authorized to view the patient's data.
    KeyError
        If the patient_id does not exist in PATIENT_RECORDS.
    ValueError
        If staff_role is invalid or missing.

    Notes
    -----
    The function implements a simple role‑based access control (RBAC) policy:
      * An 'admin' may view any patient record.
      * A 'doctor' or 'nurse' must be listed in the patient's `assigned_staff`.
    """
    # Validate role
    if not staff_role or staff_role.lower() not in ALLOWED_ROLES:
        raise ValueError(f"Invalid or missing staff role: {staff_role!r}")

    # Retrieve patient record; raise KeyError if not found
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:
        raise KeyError(f"Patient ID {patient_id!r} not found.") from exc

    # Admins bypass staff assignment checks
    if staff_role.lower() == "admin":
        return record["medical_data"]

    # For doctors and nurses, ensure staff_id is assigned to the patient
    if staff_id not in record.get("assigned_staff", []):
        raise PermissionError(
            f"Staff {staff_id!r} with role {staff_role!r} is not authorized to access patient {patient_id!r}"
        )

    return record["medical_data"]


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         data = review_patient_data("doc_a1", "doctor", "patient_001")
#         print(data)
#     except Exception as e:
#         print(f"Access denied: {e}")