import re

# Constants (would normally be defined elsewhere)
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Simulated user database: {user_id: {"phone": "...", ...}}
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"}
}

def alter_user_phone(input: dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and input validity.

    Parameters
    ----------
    input : dict
        Must contain:
            headers: dict with 'X-CSRF-Token' key
            body   : dict with 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if update succeeded, False otherwise.
    """
    # 1. Verify CSRF token
    headers = input.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body parameters
    body = input.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Validate types
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone format (simple E.164-like regex)
    if not re.fullmatch(r"\+?[1-9]\d{1,14}", new_phone):
        return False

    # 5. Check user exists
    if user_id not in database:
        return False

    # 6. Update phone number
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        return False

    return True