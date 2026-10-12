import re
from typing import Dict

# Mock database: user_id -> {'phone': str, ...}
database: Dict[int, dict] = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN = "secure_token_123"

def _is_valid_phone(phone: str) -> bool:
    """
    Very basic phone validation. Accepts + followed by 10-15 digits.
    """
    return bool(re.fullmatch(r"\+\d{10,15}", phone))

def alter_user_phone(incoming_request: Dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    incoming_request : dict
        Expected to contain:
            - headers: dict, must include 'X-CSRF-Token'
            - body:   dict, must contain 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or invalid.
    """
    # 1. Verify CSRF token
    headers = incoming_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract body data
    body = incoming_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if user_id is None or new_phone is None:
        return False

    # 3. Validate types
    if not isinstance(user_id, int):
        return False

    # 4. Validate phone format
    if not isinstance(new_phone, str) or not _is_valid_phone(new_phone):
        return False

    # 5. Update database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True