import re

# Mock database and CSRF token for the example
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob", "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def _is_valid_phone(phone: str) -> bool:
    """
    Very simple phone validation: must start with '+' followed by 10-15 digits.
    Adjust as needed for your real-world validation rules.
    """
    return bool(re.fullmatch(r"\+\d{10,15}", phone))

def change_user_phone(request_details: dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    request_details : dict
        Dictionary containing request headers and body. Expected keys:
            - 'headers': mapping of header names to values.
            - 'body': mapping containing 'user_id' (int) and 'new_phone' (str).

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    try:
        headers = request_details.get("headers", {})
        body = request_details.get("body", {})

        # CSRF protection
        csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # Extract user ID and new phone number
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        # Basic validation
        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        if not _is_valid_phone(new_phone):
            return False

        # Ensure user exists
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Update the phone number
        user_record["phone"] = new_phone
        return True

    except Exception:
        # Do not expose internal errors; simply indicate failure.
        return False