import re

# Mock database and CSRF token (in real code these would be secure, persistent storage)
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"}
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Regular expression for a simple E.164 phone number format (e.g., +15551234567)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def alter_user_phone(incoming_request: dict) -> bool:
    """
    Update a user's phone number after validating CSRF token, user ID and phone format.

    Parameters
    ----------
    incoming_request : dict
        Expected to contain:
            headers: dict with 'X-CSRF-Token'
            body   : dict with keys 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = incoming_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or invalid
        return False

    # 2. Extract and validate body contents
    body = incoming_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # Validate user_id is an integer and exists in the database
    if not isinstance(user_id, int) or user_id not in database:
        return False

    # Validate phone number format
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 3. Perform the update
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # In a real application, log the exception securely.
        return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": "secure_token_123"},
        "body": {"user_id": 1, "new_phone": "+15559876543"}
    }
    print(alter_user_phone(req))  # Should output: True
    print(database[1]["phone"])   # Updated phone number