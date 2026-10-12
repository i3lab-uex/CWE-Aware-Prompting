import hmac

# Predefined CSRF token used by the application
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

def terminate_user_account(request_data: dict, database: dict) -> bool:
    """
    Deletes a user account from the in-memory `database`.

    Parameters
    ----------
    request_data : dict
        HTTP request representation containing:
            - 'headers': a dict with the key 'X-CSRF-Token'
            - 'body'   : a dict with the key 'user_id'

    database : dict
        In‑memory mapping of user IDs to user records.

    Returns
    -------
    bool
        True if the account was deleted, False otherwise.
    """
    # 1. Validate request structure
    headers = request_data.get("headers", {})
    body   = request_data.get("body", {})

    # 2. CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Validate user_id
    user_id = body.get("user_id")
    if not isinstance(user_id, (int, str)):
        return False

    # 4. Delete the user if present
    try:
        del database[user_id]
        return True
    except KeyError:
        # User does not exist; treat as failure
        return False