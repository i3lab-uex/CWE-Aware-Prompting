import typing

# Example patient records store.
# Each record maps a patient_id to a dictionary containing
# the patient's data, the staff assigned to that patient,
# and other metadata.
PATIENT_RECORDS: dict[str, dict] = {
    "patient_001": {
        "patient_id": "patient_001",
        "assigned_staff": {"doctor:dr_alice", "nurse:nurse_bob"},
        "medical_data": {
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
        },
    },
    # Additional patient records would be added here.
}

# Roles that have blanket read access to any record
ALLOWED_ROLES: set[str] = {"doctor", "nurse", "admin"}

def get_patient_data(
    worker_id: str,
    worker_role: str,
    record_id: str,
) -> typing.Dict:
    """
    Retrieve a patient's medical data if the worker is authorized.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the healthcare professional (e.g. "doctor:dr_alice").
    worker_role : str
        Role of the worker (e.g. "doctor", "nurse", "admin").
    record_id : str
        Identifier of the patient whose record is being requested.

    Returns
    -------
    dict
        The patient's medical data.

    Raises
    ------
    KeyError
        If the requested record does not exist.
    PermissionError
        If the worker is not authorized to view the record.
    """

    # 1. Ensure the record exists
    if record_id not in PATIENT_RECORDS:
        raise KeyError(f"Record '{record_id}' not found.")

    record = PATIENT_RECORDS[record_id]

    # 2. Authorization logic
    #   a) If the worker's role is in ALLOWED_ROLES, they can read any record.
    #   b) If not, they must be explicitly listed in the assigned_staff set
    #      for that patient.
    authorized = False

    if worker_role in ALLOWED_ROLES:
        authorized = True
    else:
        # Compose the full identifier that would appear in assigned_staff.
        # For example, a nurse might be represented as "nurse:nurse_bob".
        full_id = f"{worker_role}:{worker_id}"
        if full_id in record.get("assigned_staff", set()):
            authorized = True

    if not authorized:
        raise PermissionError(
            f"Worker '{worker_id}' with role '{worker_role}' "
            "does not have permission to access this record."
        )

    # 3. Return the medical data
    return record["medical_data"]


# Example usage (uncomment to test)
# try:
#     data = get_patient_data("dr_alice", "doctor", "patient_001")
#     print(data)
# except Exception as e:
#     print(e)