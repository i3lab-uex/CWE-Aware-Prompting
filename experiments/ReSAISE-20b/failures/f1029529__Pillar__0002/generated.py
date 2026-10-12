import re

# Mock database: user_id -> dict of user details (including 'phone')
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"}
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-token-12345"

def _is_valid_phone(phone: str) -> bool:
    """
    Basic phone number validation.
    Accepts international format starting with '+' followed by 10-15 digits.
    """
    return bool(re.fullmatch(r"\+\d{10,15}", phone))

def modify_user_phone(client_request: dict) -> bool:
    """
    Update the phone number of a user in the mock database.

    Parameters
    ----------
    client_request : dict
        Must contain:
            - headers: dict, including 'X-CSRF-Token'
            - body: dict, with keys 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. CSRF protection
    headers = client_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract and validate request body
    body = client_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = body["new_phone"]
    except (KeyError, ValueError):
        return False

    # 3. Validate phone number format
    if not _is_valid_phone(new_phone):
        return False

    # 4. Verify user exists in the database
    if user_id not in database:
        return False

    # 5. Perform the update
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        # Any unexpected error during update should not expose internal state
        return False

    return True