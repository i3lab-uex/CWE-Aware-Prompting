import re
from typing import Dict

# Simulated global context (would normally be injected or imported)
database: Dict[int, dict] = {}
EXPECTED_CSRF_TOKEN: str = "known_csrf_token_value"

# Regular expression for a simple phone number validation (digits, optional +, length 7-15)
PHONE_REGEX = re.compile(r"^\+?\d{7,15}$")


def change_user_phone(payload: Dict) -> bool:
    """
    Update a user's phone number after validating the CSRF token and input data.

    Parameters
    ----------
    payload : dict
        A request dictionary containing:
            - headers: dict with key 'X-CSRF-Token'
            - body: dict with keys 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # --- 1. Validate CSRF token -------------------------------------------------
    try:
        headers = payload["headers"]
        csrf_token = headers.get("X-CSRF-Token")
    except (KeyError, AttributeError):
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token mismatch
        return False

    # --- 2. Extract and validate body parameters ---------------------------------
    try:
        body = payload["body"]
        user_id_raw = body.get("user_id")
        new_phone_raw = body.get("new_phone")
    except (KeyError, AttributeError):
        return False

    # Ensure user_id is an integer
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    # Ensure new_phone is a string and matches the expected format
    if not isinstance(new_phone_raw, str) or not PHONE_REGEX.fullmatch(new_phone_raw):
        return False

    # --- 3. Update the database entry -------------------------------------------
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        # User does not exist or record is malformed
        return False

    # Perform the update atomically (in a real DB this would be a transaction)
    user_record["phone"] = new_phone_raw
    database[user_id] = user_record

    return True