import re

# Predefined CSRF token for the application (should be securely stored in a real system)
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token"

# Simulated user database: {user_id: {"phone": str, ...}}
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}

# Regular expression for a basic E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def alter_user_phone(input: dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input data.

    Args:
        input: dict containing headers (with 'csrf_token') and body
               {'user_id': int, 'new_phone': str}

    Returns:
        bool: True if the update succeeds, False otherwise.
    """
    # 1. Validate CSRF token
    headers = input.get("headers", {})
    csrf_token = headers.get("csrf_token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = input.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic type checks
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Check that the user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Perform the update
    try:
        user_record["phone"] = new_phone
    except Exception:  # Catch unexpected errors during assignment
        return False

    return True