import re

# Simulated database: user_id -> user record dict
database = {
    1: {"name": "Alice", "phone": "555-1234"},
    2: {"name": "Bob", "phone": "555-5678"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure_csrf_token_value"

def update_user_phone(request: dict) -> bool:
    """
    Update a user's phone number.

    Parameters
    ----------
    request : dict
        Expected keys:
            - "headers": dict containing HTTP headers.
                Must include 'X-CSRF-Token'.
            - "body": dict with:
                - "user_id" : int
                - "new_phone" : str

    Returns
    -------
    bool
        True if the phone number was updated successfully,
        False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID and new phone number
    body = request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Validate phone number format (simple E.164 or local pattern)
    # Here we accept digits, spaces, dashes, parentheses, and plus sign.
    phone_pattern = re.compile(r"^\+?[\d\s\-\(\)]+$")
    if not phone_pattern.match(new_phone):
        return False

    # 4. Ensure user exists
    if user_id not in database:
        return False

    # 5. Update the phone number
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        return False

    return True