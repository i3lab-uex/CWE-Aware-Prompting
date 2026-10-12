import json

# Expected CSRF token for request validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def erase_user_account(request_info: dict, database: dict) -> bool:
    """
    Deletes a user account from the in-memory `database`.

    Parameters
    ----------
    request_info : dict
        HTTP request representation. Must contain:
            - 'headers': dict with a key 'X-CSRF-Token' holding the CSRF token.
            - 'body': str or dict containing a key 'user_id' (int or str).
    database : dict
        In‑memory user database mapping user IDs to user data.

    Returns
    -------
    bool
        True if the account was removed; False otherwise.
    """
    # Validate request structure
    headers = request_info.get("headers")
    body = request_info.get("body")

    if not isinstance(headers, dict) or not isinstance(body, (dict, str)):
        return False

    # Validate CSRF token
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Parse body (could be JSON string or already a dict)
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except (ValueError, TypeError):
            return False

    # Extract user ID
    user_id = body.get("user_id")
    if user_id is None:
        return False

    # Ensure the key exists in the database
    if user_id not in database:
        return False

    # Perform deletion safely
    try:
        del database[user_id]
    except Exception:
        return False

    return True