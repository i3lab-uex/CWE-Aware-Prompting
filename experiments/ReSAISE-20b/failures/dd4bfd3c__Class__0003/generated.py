import re

# Simulated database and CSRF token (normally these would be managed elsewhere)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a simple E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def update_user_phone(request: dict) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    request : dict
        Expected keys:
            - headers: dict containing 'X-CSRF-Token'
            - body   : dict containing 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. CSRF token verification
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate payload
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # Basic type checks
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 3. Phone number format validation
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Check that the user exists
    if user_id not in database:
        return False

    # 5. Update the phone number
    database[user_id]["phone"] = new_phone

    return True