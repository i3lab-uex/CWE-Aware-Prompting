import re

# Sample user database: {user_id (int): {"phone": str, ...}}
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"},
}

# Expected CSRF token configured on the server
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Regular expression for a simple E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")


def modify_user_phone(user_request: dict) -> bool:
    """
    Update the phone number for a user after validating CSRF token and input format.

    Args:
        user_request (dict): Dictionary containing headers and a body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "..."},
                    "body":    {"user_id": 1, "new_phone": "+11234567890"}
                }

    Returns:
        bool: True if the phone number was updated, False otherwise.

    Raises:
        ValueError: If required fields are missing or invalid.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False  # CSRF validation failed

    # 2. Extract and validate body parameters
    body = user_request.get("body", {})
    if not isinstance(body, dict):
        return False

    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError, TypeError):
        return False  # Missing or malformed fields

    if not PHONE_REGEX.match(new_phone):
        return False  # Phone number format invalid

    # 3. Update the database
    user_record = database.get(user_id)
    if not user_record:
        return False  # User does not exist

    # Optional: enforce that the new phone is different
    if user_record.get("phone") == new_phone:
        return True  # No change needed, but operation is considered successful

    user_record["phone"] = new_phone
    return True


# Example usage:
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": "secure_csrf_token_123"},
        "body":    {"user_id": 1, "new_phone": "+15555550123"}
    }
    success = modify_user_phone(request)
    print("Update successful:", success)
    print("Updated record:", database[1])