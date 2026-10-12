import re

# Simulated database of users: {user_id: {"phone": str, ...}}
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
}

# Expected CSRF token that the client must provide
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def update_user_phone(request: dict) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    request : dict
        Expected to contain:
            - 'headers': dict, must include 'X-CSRF-Token'
            - 'body'   : dict, must include 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.

    Raises
    ------
    ValueError
        If the request structure is invalid or missing required fields.
    """
    # 1. Validate CSRF token
    headers = request.get("headers")
    if not isinstance(headers, dict):
        return False

    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Validate body
    body = request.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 3. Validate phone format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Check user exists
    if user_id not in database:
        return False

    # 5. Update phone number
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Log exception in real application
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15559990000"},
    }
    print(update_user_phone(req))  # Should output: True
    print(database[1]["phone"])   # Should show the updated phone number