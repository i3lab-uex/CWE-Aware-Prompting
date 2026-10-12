import re

# Mock database and expected CSRF token for the example
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def modify_user_phone(client_request: dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and input validity.

    Args:
        client_request: A dict containing 'headers' (dict) and 'body' (dict).
            The body must include:
                - 'user_id': int
                - 'new_phone': str

    Returns:
        True if the update succeeded, False otherwise.
    """
    # 1. Validate request structure
    headers = client_request.get("headers", {})
    body   = client_request.get("body", {})

    # 2. CSRF token verification
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False  # CSRF check failed

    # 3. Extract and validate user_id
    try:
        user_id = int(body.get("user_id"))
    except (TypeError, ValueError):
        return False  # Invalid or missing user_id

    if user_id not in database:
        return False  # User does not exist

    # 4. Validate phone number format (simple E.164 check)
    new_phone = body.get("new_phone")
    if not isinstance(new_phone, str):
        return False

    # E.164 regex: optional '+' followed by 10-15 digits
    if not re.fullmatch(r"\+?[1-9]\d{9,14}", new_phone):
        return False

    # 5. Perform the update
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        return False  # Unexpected error during update

    return True