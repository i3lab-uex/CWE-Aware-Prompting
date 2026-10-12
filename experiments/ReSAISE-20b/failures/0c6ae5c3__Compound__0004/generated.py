import json

# Predefined CSRF token used by the application
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

def erase_user_account(request_info: dict, database: dict) -> bool:
    """
    Deletes a user account from the in-memory `database` if the request
    contains a valid CSRF token and a valid user ID.

    Parameters
    ----------
    request_info : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing the CSRF token under
                         key 'X-CSRF-Token'.
            - 'body': dict or JSON string containing the key
                      'user_id' that identifies the user to delete.
    database : dict
        In‑memory dictionary simulating a user database. Keys are user IDs.

    Returns
    -------
    bool
        True if the account was found and deleted, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_info.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract user ID from body
    body = request_info.get("body")
    if body is None:
        return False

    # Body may be a dict or a JSON string
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return False

    user_id = body.get("user_id")
    if user_id is None:
        return False

    # 3. Attempt to delete the user
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False