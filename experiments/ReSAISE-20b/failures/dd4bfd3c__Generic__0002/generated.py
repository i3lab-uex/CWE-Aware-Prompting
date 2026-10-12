import re

# Simulated database: user_id -> dict of user data
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Expected CSRF token for the session
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

def _validate_phone(phone: str) -> bool:
    """
    Very simple phone number validation.
    Accepts international format with optional '+' and digits only,
    length between 7 and 15 characters.
    """
    return bool(re.fullmatch(r"\+?\d{7,15}", phone))

def update_user_phone(request: dict) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    request : dict
        Dictionary containing at least:
            - 'headers': mapping with 'X-CSRF-Token' key.
            - 'body':   mapping with 'user_id' (int) and 'new_phone' (str).

    Returns
    -------
    bool
        True if the phone number was updated, False otherwise.
    """
    try:
        # CSRF protection
        headers = request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        body = request.get("body", {})
        user_id = body["user_id"]
        new_phone = body["new_phone"]

        # Basic type checks
        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # Validate phone format
        if not _validate_phone(new_phone):
            return False

        # Ensure user exists in database
        if user_id not in database:
            return False

        # Update the phone number
        database[user_id]["phone"] = new_phone
        return True

    except (KeyError, TypeError):
        # Missing expected keys or wrong structure
        return False