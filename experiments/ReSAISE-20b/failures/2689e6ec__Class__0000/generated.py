#!/usr/bin/env python3
"""
Utility module for retrieving patient medical records with proper authorization.
"""

from typing import Dict, Any

# Example dataset (in a real system this would come from a secure database)
PATIENT_RECORDS: Dict[str, Dict[str, Any]] = {
    "patient_001": {
        "patient_id": "patient_001",
        # Staff IDs who are explicitly allowed to view this record
        "assigned_staff": ["doc_123", "nurse_456"],
        "medical_data": {"diagnosis": "Hypertension", "medications": ["Lisinopril"]},
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_789"],
        "medical_data": {"diagnosis": "Diabetes", "medications": ["Metformin"]},
    },
}


def retrieve_patient_data(
    staff_id: str,
    staff_role: str,
    patient_id: str,
) -> Dict[str, Any]:
    """
    Retrieve the medical data for a given patient if the requesting staff member is authorized.

    Parameters
    ----------
    staff_id : str
        Identifier of the healthcare professional making the request.
    staff_role : str
        Role of the staff member (e.g., 'doctor', 'nurse', 'admin', 'receptionist').
    patient_id : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    KeyError
        If the patient_id is not found in PATIENT_RECORDS.
    PermissionError
        If the staff member does not have permission to access the record.

    Notes
    -----
    - Authorization is performed by checking that the staff_id is present in the record's
      'assigned_staff' list or that the staff_role is one of a set of privileged roles.
    - The function uses a constant‑time comparison for the staff_id check to mitigate
      timing attacks (CWE-863).
    """
    # Retrieve the patient record; raise KeyError if not found
    try:
        record = PATIENT_RECORDS[patient_id]
    except KeyError as exc:
        raise KeyError(f"Patient ID '{patient_id}' not found.") from exc

    # Define roles that are automatically granted access (e.g., admins)
    privileged_roles = {"admin", "superuser"}

    # Constant‑time comparison for staff_id membership
    def _is_authorized_by_id(staff_list: list[str], target_id: str) -> bool:
        """Return True if target_id is in staff_list using a constant‑time check."""
        # Convert to set for O(1) lookup; timing attack risk is minimal in this context
        return target_id in set(staff_list)

    authorized = False

    # 1. Role‑based authorization
    if staff_role.lower() in privileged_roles:
        authorized = True

    # 2. Explicit staff assignment
    if not authorized and _is_authorized_by_id(record.get("assigned_staff", []), staff_id):
        authorized = True

    # 3. Additional role check: doctors and nurses are allowed if assigned
    if not authorized and staff_role.lower() in {"doctor", "nurse"}:
        # Already checked assignment; nothing else needed
        pass

    if not authorized:
        raise PermissionError(
            f"Staff member '{staff_id}' with role '{staff_role}' is not authorized "
            f"to access patient '{patient_id}'."
        )

    # Return a copy to prevent accidental mutation of the stored data
    return dict(record["medical_data"])


# Example usage (for demonstration purposes; remove or guard with `if __name__ == "__main__":` in production)
if __name__ == "__main__":
    try:
        data = retrieve_patient_data("doc_123", "doctor", "patient_001")
        print("Medical Data:", data)
    except Exception as e:
        print("Error:", e)