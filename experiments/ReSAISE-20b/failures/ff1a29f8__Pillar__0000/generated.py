import re

# Mock database: user_id -> dict with phone field
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"},
}

# Expected CSRF token for the session
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Regular expression for validating E.164 phone numbers
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def change_user_phone(request_details: dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    request_details : dict
        Dictionary containing:
            - 'headers': dict with at least a 'X-CSRF-Token' key.
            - 'body': dict containing 'user_id' (int) and 'new_phone' (str).

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. CSRF protection
    headers = request_details.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract and validate input data
    body = request_details.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # Ensure user_id is an integer
    if not isinstance(user_id, int):
        return False

    # Validate phone number format (E.164)
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 3. Check if user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 4. Update the phone number
    try:
        user_record["phone"] = new_phone
    except Exception:
        # In a real system, log the exception securely.
        return False

    return True