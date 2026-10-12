import re

# Sample in‑memory database: user_id -> {'phone': str, ...}
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
}

# CSRF token that the application expects
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token-123"

# Regular expression for a basic E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")

def alter_user_phone(service_request: dict) -> bool:
    """
    Update the phone number of a user after validating CSRF token and input data.

    Args:
        service_request (dict): Dictionary containing 'headers' and 'body'.
            Expected keys in body: 'user_id', 'new_phone'.

    Returns:
        bool: True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = service_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract and validate body parameters
    body = service_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # Ensure user_id is an integer
    if not isinstance(user_id, int):
        return False

    # Validate phone number format (basic E.164)
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 3. Check if user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 4. Update the phone number
    try:
        user_record["phone"] = new_phone
        return True
    except Exception:
        # Log exception in real application; here we simply fail silently
        return False

# Example usage:
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15559998888"}
    }
    print(alter_user_phone(req))  # Should output: True