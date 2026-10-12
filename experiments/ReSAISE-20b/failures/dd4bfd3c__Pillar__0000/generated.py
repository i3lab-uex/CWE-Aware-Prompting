import re

# Simulated database: user_id -> user record dict
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Expected CSRF token for this request context
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a simple E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def update_user_phone(request: dict) -> bool:
    """
    Update the phone number of a user identified by `user_id` in the request body.

    The function performs:
      * CSRF token validation
      * Basic input sanitization and type checks
      * Phone number format validation (E.164)
      * Existence check for the user in `database`

    Parameters
    ----------
    request : dict
        Dictionary containing:
            headers: dict with 'X-CSRF-Token' key.
            body:   dict with 'user_id' (int) and 'new_phone' (str).

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body parameters
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # Ensure user_id is an integer
    if not isinstance(user_id, int):
        return False

    # Ensure new_phone is a string and matches the regex
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 3. Check that the user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 4. Update the phone number
    try:
        user_record["phone"] = new_phone
        return True
    except Exception:
        # Catch unexpected errors without exposing details
        return False