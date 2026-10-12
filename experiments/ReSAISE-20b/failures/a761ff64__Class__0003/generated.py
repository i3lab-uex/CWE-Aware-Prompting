import re
from typing import Dict

# Pre‑defined CSRF token that must be supplied in the request headers
EXPECTED_CSRF_TOKEN: str = "12345-abcde"

# Simulated user database
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice",   "phone": "+15551234567"},
    2: {"name": "Bob",     "phone": "+15557654321"},
    # ... other users
}

def _is_valid_phone(phone: str) -> bool:
    """
    Basic validation for phone numbers.
    Accepts digits, optional leading '+', and length between 10 and 15.
    """
    if not isinstance(phone, str):
        return False
    pattern = r"^\+?\d{10,15}$"
    return re.match(pattern, phone) is not None

def alter_user_phone(input: Dict) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Parameters
    ----------
    input : dict
        Request dictionary containing:
            - headers: dict with a 'X-CSRF-Token' key
            - body   : dict with keys 'user_id' and 'new_phone'

    Returns
    -------
    bool
        True if the phone number was updated successfully,
        False otherwise.
    """
    # 1. Verify CSRF token
    headers = input.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or invalid
        return False

    # 2. Extract body data
    body = input.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Validate user ID
    if not isinstance(user_id, int):
        return False

    # 4. Validate phone number
    if not _is_valid_phone(new_phone):
        return False

    # 5. Check that the user exists
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # 6. Update the phone number
    try:
        user_record["phone"] = new_phone
    except Exception:
        # Any unforeseen error during update results in failure
        return False

    return True