import re

# Mock database and CSRF token (would normally be provided by the framework)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

def _validate_csrf_token(token: str) -> bool:
    """Simple CSRF token validation."""
    return token == EXPECTED_CSRF_TOKEN

def _validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format.
    Accepts numbers with optional + sign and 10-15 digits.
    """
    pattern = re.compile(r"^\+?\d{10,15}$")
    return bool(pattern.match(phone))

def alter_user_phone(incoming_request: dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    incoming_request : dict
        Dictionary representing an HTTP request. Expected keys:
            - "headers": {"X-CSRF-Token": str}
            - "body":   {"user_id": int, "new_phone": str}

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # Basic structure validation
    headers = incoming_request.get("headers", {})
    body   = incoming_request.get("body", {})

    # CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not _validate_csrf_token(csrf_token):
        return False

    # Extract and validate user ID
    try:
        user_id = int(body.get("user_id"))
    except (TypeError, ValueError):
        return False

    # Validate new phone number
    new_phone = body.get("new_phone")
    if not isinstance(new_phone, str) or not _validate_phone_number(new_phone):
        return False

    # Check that user exists
    if user_id not in database:
        return False

    # Perform the update
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:  # pragma: no cover
        # In a real system we would log this exception.
        return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": "secure-token-123"},
        "body":   {"user_id": 1, "new_phone": "+15551234567"},
    }
    print(alter_user_phone(req))  # Expected: True
    print(database[1]["phone"])   # Expected: "+15551234567"