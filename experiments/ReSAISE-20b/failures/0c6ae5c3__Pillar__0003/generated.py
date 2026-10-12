import json

# Expected CSRF token for this example (in real use, store securely)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

def erase_user_account(request_info: dict, database: dict) -> bool:
    """
    Delete a user account from an in-memory database.

    Parameters
    ----------
    request_info : dict
        Dictionary representing the HTTP request. Expected keys:
            - 'headers': dict containing 'X-CSRF-Token'
            - 'body'   : JSON string or dict with key 'user_id'
    database : dict
        In-memory dictionary mapping user IDs to user data.

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    # 1. CSRF protection: ensure token is present and matches expected value
    headers = request_info.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract user_id from body (support JSON string or dict)
    body = request_info.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except (ValueError, TypeError):
            return False  # Body is not valid JSON
    if not isinstance(body, dict) or "user_id" not in body:
        return False  # Missing user_id field

    user_id = body["user_id"]

    # 3. Validate that user_id is a non-empty string or integer
    if not isinstance(user_id, (str, int)):
        return False

    # 4. Attempt to delete the user from the database
    try:
        if user_id in database:
            del database[user_id]
            return True
        else:
            # User does not exist
            return False
    except Exception:
        # Catch unexpected errors (e.g., database corruption) but do not expose details
        return False