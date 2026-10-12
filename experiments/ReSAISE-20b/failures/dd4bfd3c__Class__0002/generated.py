import re

# Simulated database: mapping user_id -> dict with phone number and other fields
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}

# Expected CSRF token for the session
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token-123"

# Regular expression for a simple international phone number (E.164 format)
PHONE_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")

def update_user_phone(request: dict) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    request : dict
        Expected to contain:
            - headers: dict with 'X-CSRF-Token'
            - body:   dict with keys 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Validate body presence
    body = request.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 3. Verify user exists
    if user_id not in database:
        return False

    # 4. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Update the database
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Any unexpected failure should be treated as a failure
        return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    request_example = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15559998888"}
    }
    print(update_user_phone(request_example))  # Should output: True