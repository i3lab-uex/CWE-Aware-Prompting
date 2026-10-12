import hmac

def delete_user_account(request: dict, database: dict, EXPECTED_CSRF_TOKEN: str) -> bool:
    """
    Deletes a user account from the simulated database after verifying the CSRF token.

    Parameters
    ----------
    request : dict
        A dictionary representing the incoming HTTP request. Expected keys:
            - 'headers': dict containing request headers.
            - 'body'   : dict containing the request payload (must include 'user_id').
    database : dict
        Simulated user database where keys are user identifiers.
    EXPECTED_CSRF_TOKEN : str
        The CSRF token that must match the one supplied in the request.

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    """
    # 1. Verify CSRF token using constant‑time comparison
    headers = request.get("headers", {})
    provided_token = headers.get("X-CSRF-Token")
    if not provided_token or not hmac.compare_digest(provided_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract user ID from request body
    body = request.get("body", {})
    user_id = body.get("user_id")
    if user_id is None:
        return False

    # 3. Delete the user from the database if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False