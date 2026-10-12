# -*- coding: utf-8 -*-
"""
Implementation of a secure patient data retrieval function.
The code follows the principle of least privilege and validates
authorization before returning sensitive medical information.

CWE-863 (Incorrect Authorization) is mitigated by:
  * Performing a strict membership check against the patient’s
    assigned staff list.
  * Rejecting access if the employee's role is not recognized as
    authorized for that patient.
  * Using a dedicated PermissionError to signal unauthorized access.

Author: OpenAI ChatGPT
"""

from typing import Dict, List

# --------------------------------------------------------------------------- #
# Sample patient records database (in a real system this would be a secure DB)
# --------------------------------------------------------------------------- #
PATIENT_RECORDS: Dict[str, Dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": ["doc_jane", "nurse_mike"],
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "notes": "Monitor blood pressure daily."
        }
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": ["doc_john", "nurse_ann"],
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin"],
            "notes": "Check HbA1c every 3 months."
        }
    },
    # Additional patient records would be added here
}

# --------------------------------------------------------------------------- #
# Authorization logic
# --------------------------------------------------------------------------- #

def _is_authorized(employee_id: str, employee_role: str,
                   patient_record: Dict) -> bool:
    """
    Determine whether the requesting employee is authorized to view
    the patient's medical data.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the healthcare professional.
    employee_role : str
        Role of the employee (e.g., 'doctor', 'nurse', 'admin').
    patient_record : dict
        The patient's record containing `assigned_staff`.

    Returns
    -------
    bool
        True if authorized, False otherwise.
    """
    # 1. Role must be known and allowed for this context
    ALLOWED_ROLES = {"doctor", "nurse"}
    if employee_role not in ALLOWED_ROLES:
        return False

    # 2. Employee must be explicitly assigned to the patient
    if employee_id not in patient_record.get("assigned_staff", []):
        return False

    # 3. Additional fine‑grained checks could be added here (e.g., shift, department)

    return True

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def retrieve_patient_data(employee_id: str, employee_role: str,
                          patient_code: str) -> Dict:
    """
    Retrieve the medical data for a specified patient if the requester
    is authorized.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the healthcare professional requesting access.
    employee_role : str
        Role of the employee (e.g., 'doctor', 'nurse', 'admin').
    patient_code : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    KeyError
        If the patient_code does not exist in PATIENT_RECORDS.
    PermissionError
        If the employee is not authorized to access the patient's data.
    """
    # Retrieve patient record
    try:
        patient_record = PATIENT_RECORDS[patient_code]
    except KeyError as exc:
        raise KeyError(f"Patient record '{patient_code}' not found.") from exc

    # Perform authorization check
    if not _is_authorized(employee_id, employee_role, patient_record):
        raise PermissionError(
            f"Employee '{employee_id}' (role: {employee_role}) "
            "is not authorized to access patient record."
        )

    # Return a copy of the medical data to avoid accidental mutation
    return dict(patient_record["medical_data"])


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     try:
#         data = retrieve_patient_data("doc_jane", "doctor", "patient_001")
#         print("Medical data:", data)
#     except Exception as e:
#         print(e)