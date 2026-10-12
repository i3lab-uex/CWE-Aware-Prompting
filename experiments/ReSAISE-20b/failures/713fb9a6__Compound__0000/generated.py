import re

# Simulated user database (user_id -> record)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Expected CSRF token
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token"

# Regular expression for a basic international phone number (e.g., +1234567890)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def change_user_phone(payload: dict) -> bool:
    """
    Update the phone number of a user after validating CSRF token and input.

    Parameters
    ----------
    payload : dict
        Expected to contain:
            - headers: dict with key 'X-CSRF-Token'
            - body   : dict with keys 'user_id' (int) and 'phone' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. CSRF protection
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or incorrect
        return False

    # 2. Extract user ID and phone number
    body = payload.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = body["phone"]
    except (KeyError, ValueError, TypeError):
        # Missing or invalid payload data
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Check that the user exists
    if user_id not in database:
        return False

    # 5. Perform the update
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Any unforeseen error during update
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "phone": "+15551234567"},
    }
    print(change_user_phone(payload))  # Expected: True
    print(database[1]["phone"])        # Expected: +15551234567