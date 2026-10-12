import re

# Simulated database of users (user_id: {name, phone})
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"}
}

# Expected CSRF token (would normally be stored per session)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_value"

# Regular expression to validate international phone numbers (basic check)
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")  # E.164 format


def update_user_phone(request: dict) -> bool:
    """
    Update the phone number for a user if the request is valid.

    Args:
        request (dict): A dictionary containing 'headers' and 'body'.
            Expected keys in headers: 'X-CSRF-Token'
            Expected keys in body: 'user_id', 'new_phone'

    Returns:
        bool: True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    csrf_token = request.get("headers", {}).get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate payload
    body = request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError):
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Check that the user exists
    if user_id not in database:
        return False

    # 5. Update the phone number
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        return False

    return True