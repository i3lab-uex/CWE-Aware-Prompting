import re

# Simulated database: user_id -> { "phone": "...", ... }
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Expected CSRF token (would normally be stored per session)
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")  # e.g., +1234567890


def update_user_phone(request: dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input format.

    Parameters
    ----------
    request : dict
        Expected keys:
            - headers: dict containing 'X-CSRF-Token'
            - body   : dict containing 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    try:
        headers = request.get("headers", {})
        body = request.get("body", {})

        # 1. CSRF protection
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract user ID and new phone number
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # 3. Validate phone number format
        if not PHONE_REGEX.match(new_phone):
            return False

        # 4. Check that the user exists
        if user_id not in database:
            return False

        # 5. Perform the update
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # Log exception in real application; swallow and fail safely here
        return False


# Example usage (would normally be part of a test or request handler)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15551234567"},
    }
    success = update_user_phone(req)
    print("Update successful:", success)
    print("New database state:", database[1])