import json

# Preconfigured CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Sample user database: {user_id: {"phone": <number>, ...}}
database = {
    "1": {"name": "Alice", "phone": "+1234567890"},
    "2": {"name": "Bob",   "phone": "+0987654321"}
}

def modify_user_phone(user_request: dict) -> bool:
    """
    Update a user's phone number in the `database`.

    Parameters
    ----------
    user_request : dict
        Expected format:
        {
            "headers": {"X-CSRF-Token": "<token>"},
            "body":   '{"user_id":"1","new_phone":"+1122334455"}'
        }

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Parse request body
    body_str = user_request.get("body", "")
    try:
        body = json.loads(body_str)
    except (json.JSONDecodeError, TypeError):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not user_id or not new_phone:
        return False

    # 3. Validate phone number format (simple check)
    if not isinstance(new_phone, str) or not new_phone.startswith('+') or len(new_phone) < 7:
        return False

    # 4. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Perform the update
    try:
        user_record["phone"] = new_phone
    except Exception:
        return False

    return True