#!/usr/bin/env python3
"""
Secure patient record access module.

The function `get_patient_data` performs a strict authorization check before
returning sensitive medical data.  The implementation follows the principle
of least privilege and mitigates CWE‑863 (Incorrect Authorization).
"""

from __future__ import annotations

import typing as _t
import logging

# Configure basic logger for audit purposes.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s [%(module)s:%(lineno)d] %(message)s",
)
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Sample patient records database
# --------------------------------------------------------------------------- #

PATIENT_RECORDS: dict[str, dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        # Staff assigned to this patient
        "assigned_staff": {"dr_smith", "nurse_jane"},
        # Sensitive medical data (in a real system this would be encrypted)
        "medical_data": {
            "diagnosis": "Hypertension",
            "treatment_plan": ["Medication A", "Lifestyle changes"],
        },
    },
    "patient_002": {
        "patient_id": "patient_002",
        "assigned_staff": {"dr_brown", "nurse_jane"},
        "medical_data": {
            "diagnosis": "Type 2 Diabetes",
            "treatment_plan": ["Medication B", "Dietary plan"],
        },
    },
}


# --------------------------------------------------------------------------- #
# Authorization utilities
# --------------------------------------------------------------------------- #

def _is_worker_authorized(
    worker_id: str,
    worker_role: str,
    record: dict[str, _t.Any],
) -> bool:
    """
    Determine whether a worker is authorized to access the given record.

    Rules:
        * Role 'admin' can read any record.
        * Roles 'doctor' and 'nurse' may only read records where their ID
          appears in the record's `assigned_staff` set.
        * All other roles are denied.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the worker.
    worker_role : str
        Role of the worker (e.g., 'doctor', 'nurse', 'admin').
    record : dict
        The patient record dictionary.

    Returns
    -------
    bool
        True if authorized, False otherwise.
    """
    # Normalise role string to lower case for robust comparison
    role = worker_role.strip().lower()

    if role == "admin":
        logger.debug("Admin access granted for worker %s", worker_id)
        return True

    if role in {"doctor", "nurse"}:
        authorized = worker_id in record.get("assigned_staff", set())
        logger.debug(
            "Role %s access for worker %s to record %s: %s",
            role,
            worker_id,
            record["patient_id"],
            authorized,
        )
        return authorized

    # All other roles are not permitted
    logger.debug(
        "Access denied for role %s (worker %s) to record %s",
        role,
        worker_id,
        record["patient_id"],
    )
    return False


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def get_patient_data(
    worker_id: str,
    worker_role: str,
    record_id: str,
) -> dict[str, _t.Any]:
    """
    Retrieve a patient's medical data after performing an authorization check.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the healthcare professional requesting the data.
    worker_role : str
        Role of the requester (e.g., 'doctor', 'nurse', 'admin').
    record_id : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data if the request is authorized.

    Raises
    ------
    PermissionError
        If the worker does not have permission to access the requested record.
    KeyError
        If no patient record exists for the given `record_id`.
    """
    logger.info(
        "Worker %s (%s) requesting record %s",
        worker_id,
        worker_role,
        record_id,
    )

    # Fetch the patient record; raise KeyError if missing
    try:
        record = PATIENT_RECORDS[record_id]
    except KeyError as exc:
        logger.error("Patient record %s not found", record_id)
        raise KeyError(f"Patient record '{record_id}' does not exist.") from exc

    # Perform the authorization check
    if not _is_worker_authorized(worker_id, worker_role, record):
        logger.warning(
            "Unauthorized access attempt by %s (%s) to record %s",
            worker_id,
            worker_role,
            record_id,
        )
        raise PermissionError(
            f"Worker '{worker_id}' does not have permission to access record "
            f"'{record_id}'."
        )

    # Return a copy of the medical data to avoid accidental mutation
    logger.debug("Access granted; returning data for record %s", record_id)
    return dict(record["medical_data"])


# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example: a doctor retrieving an assigned patient's record
    try:
        data = get_patient_data("dr_smith", "doctor", "patient_001")
        print("Medical data:", data)
    except Exception as exc:
        logger.exception("Error retrieving patient data: %s", exc)