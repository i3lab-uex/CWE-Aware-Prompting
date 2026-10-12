import re

# Mock database: mapping user_id (int) to a dict of attributes
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure_token_12345"

def _is_valid_phone(phone: str) -> bool:
    """
    Very simple phone validation: digits, optional + and spaces.
    Adjust the regex according to your application's rules.
    """
    return bool(re.fullmatch(r"\+?\d{7,15}", phone))

def change_user_phone(request_details: dict) -> bool:
    """
    Update a user's phone number after validating the request.

    Args:
        request_details (dict): Should contain:
            - 'headers': dict with at least a 'X-CSRF-Token' key.
            - 'body': dict with keys 'user_id' (int) and 'new_phone' (str).

    Returns:
        bool: True if the phone number was updated successfully, False otherwise.

    Raises:
        None.  Errors are handled gracefully and result in a False return.
    """
    try:
        # Validate CSRF token
        headers = request_details.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # Extract body parameters
        body = request_details.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        # Basic type checks
        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # Validate phone format
        if not _is_valid_phone(new_phone):
            return False

        # Ensure user exists
        user_record = database.get(user_id)
        if user_record is None:
            return False

        # Perform the update
        user_record["phone"] = new_phone
        return True

    except Exception:
        # Log the exception in a real application; here we simply swallow it
        return False

# Example usage (would normally be part of a test suite)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+1112223333"},
    }
    print(change_user_phone(request))  # Should output: True
    print(database[1]["phone"])        # Should show the updated phone number