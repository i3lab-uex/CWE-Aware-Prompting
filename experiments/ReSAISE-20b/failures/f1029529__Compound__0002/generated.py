import re

# Expected CSRF token value (would normally be stored securely)
EXPECTED_CSRF_TOKEN = "expected_token_value"

# Mock database: user_id -> user info dict
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Regular expression to validate international phone numbers (basic check)
PHONE_REGEX = re.compile(r"^\+\d{7,15}$")


def modify_user_phone(client_request: dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        Dictionary containing request headers and body.
        Expected keys:
            - 'headers': dict with at least 'X-CSRF-Token'
            - 'body': dict with 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. CSRF protection
    headers = client_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token; reject request
        return False

    # 2. Extract and validate body data
    body = client_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError, TypeError):
        # Missing or malformed fields
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
        # Unexpected error during update
        return False

    return True