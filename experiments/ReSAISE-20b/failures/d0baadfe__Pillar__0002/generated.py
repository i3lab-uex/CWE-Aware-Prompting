import re

# Sample user database (user_id -> dict with 'phone' field)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Preconfigured CSRF token that must match the request header
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def modify_user_phone(user_request: dict) -> bool:
    """
    Update the phone number of a user in the database.

    Parameters
    ----------
    user_request : dict
        Dictionary containing request headers and body. Expected keys:
            - 'headers': dict with a 'X-CSRF-Token' key
            - 'body': dict with 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False  # Invalid or missing CSRF token

    # 2. Extract body parameters
    body = user_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError):
        return False  # Missing or malformed fields

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False  # Phone number does not match expected pattern

    # 4. Ensure user exists in the database
    if user_id not in database:
        return False  # User does not exist

    # 5. Update the phone number
    database[user_id]["phone"] = new_phone

    return True