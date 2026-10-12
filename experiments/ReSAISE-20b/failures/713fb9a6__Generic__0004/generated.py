import re

# Simulated database: {user_id: {"phone": "...", ...}}
database = {}

# Pre‑defined CSRF token that must match the request header
EXPECTED_CSRF_TOKEN = "my_secure_token_123"

def change_user_phone(payload: dict) -> bool:
    """
    Update a user's phone number after validating the CSRF token.

    Parameters
    ----------
    payload : dict
        Request dictionary containing:
            - headers: dict with 'X-CSRF-Token'
            - body:   dict with 'user_id' and 'new_phone'

    Returns
    -------
    bool
        True if the phone number was updated, False otherwise.
    """
    # Validate payload structure
    headers = payload.get("headers", {})
    body = payload.get("body", {})

    # 1. CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID and new phone number
    try:
        user_id = body["user_id"]
        new_phone = body["new_phone"]
    except KeyError:
        return False

    # 3. Basic phone number validation (digits only, length 7-15)
    if not re.fullmatch(r"\d{7,15}", new_phone):
        return False

    # 4. Update the database if user exists
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        return False

    # Store the new phone number
    user_record["phone"] = new_phone
    return True