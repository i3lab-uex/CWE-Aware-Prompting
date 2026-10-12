import re

# Simulated database and CSRF token for the web application.
database: dict[int, dict[str, str]] = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

# Regular expression for a basic phone number validation (international format).
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def change_user_phone(payload: dict) -> bool:
    """
    Update the phone number of a user after verifying CSRF token and input validity.

    Args:
        payload: dict containing:
            - headers: dict with key 'X-CSRF-Token'
            - body: dict with keys 'user_id' (int) and 'new_phone' (str)

    Returns:
        bool: True if update succeeded, False otherwise.

    Raises:
        None
    """
    # 1. CSRF protection: verify token from headers.
    try:
        csrf_token = payload["headers"]["X-CSRF-Token"]
    except (KeyError, TypeError):
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token – possible CSRF attack.
        return False

    # 2. Extract body data safely.
    try:
        user_id = payload["body"]["user_id"]
        new_phone = payload["body"]["new_phone"]
    except (KeyError, TypeError):
        return False

    # 3. Validate data types.
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone number format.
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Check that the user exists.
    if user_id not in database:
        return False

    # 6. Perform the update atomically.
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        # Any unexpected error during update should fail gracefully.
        return False

    return True