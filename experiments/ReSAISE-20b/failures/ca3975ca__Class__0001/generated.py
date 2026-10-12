import re

# Simulated database of users: {user_id: {"phone": str, ...}}
database = {}

# Predefined CSRF token that must be present in the request headers
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a basic international phone number format
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")  # E.164 format


def modify_user_phone(request_data: dict) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Parameters
    ----------
    request_data : dict
        A dictionary containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict with keys 'user_id' and 'new_phone'

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract user ID and new phone number from body
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic validation of input types
    if not isinstance(user_id, str) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone number format (E.164)
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Check that the user exists in the database
    if user_id not in database:
        return False

    # 6. Update the phone number atomically
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        # Any unexpected error during update should result in failure
        return False

    return True