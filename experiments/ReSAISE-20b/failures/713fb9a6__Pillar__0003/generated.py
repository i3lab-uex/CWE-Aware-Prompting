import re

# Constants and simulated database (normally defined elsewhere)
EXPECTED_CSRF_TOKEN = "1234567890abcdef"
database: dict[int, dict] = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}

# Regular expression for a simple international phone number format
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def change_user_phone(payload: dict) -> bool:
    """
    Update a user's phone number after validating the CSRF token and input data.

    Args:
        payload (dict): Must contain a 'headers' dict with the key
                        'X-CSRF-Token', and a 'body' dict with keys:
                        - 'user_id': int
                        - 'new_phone': str

    Returns:
        bool: True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 3. Validate phone format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Check user existence
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Perform the update
    try:
        user_record["phone"] = new_phone
    except Exception:
        # Any unforeseen error during update should result in failure
        return False

    return True