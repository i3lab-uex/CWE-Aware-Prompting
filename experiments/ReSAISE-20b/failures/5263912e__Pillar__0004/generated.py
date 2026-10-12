import uuid

# Mock in‑memory user database: {user_id (UUID str): user_record}
database = {}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def remove_user_account(req: dict) -> bool:
    """
    Remove a user account from the in‑memory database.

    Parameters
    ----------
    req : dict
        HTTP request representation containing:
            - headers: dict, may include 'X-CSRF-Token'
            - body: dict, must contain 'user_id' (UUID string)

    Returns
    -------
    bool
        True if the account was removed, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Retrieve user ID from request body
    body = req.get("body", {})
    user_id_str = body.get("user_id")
    if not isinstance(user_id_str, str):
        return False

    # 3. Validate that the string is a valid UUID
    try:
        uuid_obj = uuid.UUID(user_id_str)
    except (ValueError, AttributeError):
        return False

    # 4. Delete the user if it exists
    if uuid_obj.hex in database:
        del database[uuid_obj.hex]
        return True

    # User not found
    return False