import re

# Sample user database: mapping from user_id to user data dict
database = {
    "user123": {"phone": "+15551234567"},
    "user456": {"phone": "+15557654321"},
}

# Preconfigured CSRF token
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"


def _validate_phone_number(phone: str) -> bool:
    """
    Very simple phone number validation.
    Accepts strings that start with an optional '+' followed by 10 to 15 digits.
    """
    return bool(re.fullmatch(r"\+?\d{10,15}", phone))


def modify_user_phone(user_request: dict) -> bool:
    """
    Update the phone number of a user in the database.

    Parameters
    ----------
    user_request : dict
        Dictionary containing at least:
            - 'headers': a mapping that may contain 'X-CSRF-Token'
            - 'body': a mapping with keys:
                * 'user_id' (str)
                * 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # Basic structure checks
    headers = user_request.get("headers", {})
    body = user_request.get("body", {})

    # 1. Verify CSRF token
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user_id and new phone
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not user_id or not new_phone:
        return False

    # 3. Validate phone format
    if not _validate_phone_number(new_phone):
        return False

    # 4. Check user exists in database
    if user_id not in database:
        return False

    # 5. Update the phone number
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Any unforeseen error should not expose internals
        return False


# Example usage (for testing purposes only):
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "new_phone": "+15550001111"},
    }
    result = modify_user_phone(request)
    print("Update successful:", result)
    print("Updated database entry:", database["user123"])