import re

# Sample database and CSRF token (would normally be stored securely)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"}
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Regular expression for a simple E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def modify_user_phone(user_request: dict) -> bool:
    """
    Update a user's phone number after validating the CSRF token and input data.

    Parameters
    ----------
    user_request : dict
        Dictionary containing request headers and body.
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "..."},
                "body":   {"user_id": 1, "new_phone": "+11234567890"}
            }

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. CSRF token validation
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = user_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError):
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Check user existence
    if user_id not in database:
        return False

    # 5. Update phone number
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        # Any unexpected error during update should be treated as failure
        return False

    return True