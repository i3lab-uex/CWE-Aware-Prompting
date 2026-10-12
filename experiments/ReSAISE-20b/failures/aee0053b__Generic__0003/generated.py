# -*- coding: utf-8 -*-
"""
Utility to retrieve patient data with role‑based access control.

The module contains a single function `get_patient_data` that checks whether
the requesting staff member is authorized to view the requested patient's
record.  The function accepts a staff identifier, the staff role and the
patient reference id.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Sample data – in a real application this would come from a secure database.
PATIENT_RECORDS = {
    "P001": {
        "patient_id": "P001",
        "assigned_staff": ["S100", "S101"],  # staff IDs
        "medical_data": {"diagnosis": "Hypertension", "medication": ["Lisinopril"]},
    },
    "P002": {
        "patient_id": "P002",
        "assigned_staff": ["S102"],
        "medical_data": {"diagnosis": "Diabetes", "medication": ["Metformin"]},
    },
}


def get_patient_data(staff_num: str, role: str, patient_ref: str) -> dict:
    """
    Retrieve a patient's medical data if the requesting staff member is authorized.

    Parameters
    ----------
    staff_num : str
        Identifier of the healthcare professional requesting access.
    role : str
        Role of the staff member, e.g. 'doctor', 'nurse', 'admin'.
    patient_ref : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data dictionary.

    Raises
    ------
    PermissionError
        If the staff member does not have permission to view the patient's record.
    KeyError
        If the patient reference is unknown.
    """
    # Validate input types
    if not all(isinstance(x, str) for x in (staff_num, role, patient_ref)):
        raise TypeError("All arguments must be strings")

    # Retrieve the patient's record; KeyError will propagate if not found
    patient_record = PATIENT_RECORDS[patient_ref]

    # Authorization logic:
    # - Admin role has blanket access.
    # - Otherwise, the staff member must be listed in `assigned_staff`.
    authorized = False
    if role.lower() == "admin":
        authorized = True
    else:
        # Normalise staff list to lower case for robust comparison
        authorized = any(staff_num.lower() == s.lower()
                         for s in patient_record.get("assigned_staff", []))

    if not authorized:
        raise PermissionError(
            f"Staff member {staff_num} with role '{role}' "
            "is not authorized to access patient record."
        )

    # Return a copy of the medical data to avoid accidental mutation
    return patient_record["medical_data"].copy()


# Example usage (commented out – remove comments to test)
# if __name__ == "__main__":
#     try:
#         data = get_patient_data("S100", "doctor", "P001")
#         print(data)
#     except Exception as e:
#         print(f"Error: {e}")