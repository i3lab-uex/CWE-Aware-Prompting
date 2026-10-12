import re

# Predefined CSRF token that must match the request header
EXPECTED_CSRF_TOKEN = "expected_csrf_token_123"

# Simulated user database: key is user_id, value is a dict with user data
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}


def _is_valid_phone(phone: str) -> bool:
    """
    Basic phone number validation.
    Accepts international numbers with optional '+' and 10-15 digits.
    """
    pattern = r"^\+?\d{10,15}$"
    return bool(re.match(pattern, phone))


def change_user_phone(payload: dict) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Parameters
    ----------
    payload : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":    {
                    "user_id": int,
                    "phone":   str
                }
            }

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # Validate CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract body data
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("phone")

    # Basic type and presence checks
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # Validate phone format
    if not _is_valid_phone(new_phone):
        return False

    # Check that the user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    try:
        user_record["phone"] = new_phone
        return True
    except Exception:
        # In a real scenario we might log the exception
        return False


# Example usage (uncomment to test)
# payload_example = {
#     "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
#     "body":    {"user_id": 1, "phone": "+11234567890"}
# }
# print(change_user_phone(payload_example))  # Should output: True