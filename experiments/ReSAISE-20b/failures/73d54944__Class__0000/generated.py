import json

# Constants
EXPECTED_CSRF_TOKEN = "expected_csrf_token_value"

def remove_user_data(data: dict, database: dict) -> bool:
    """
    Remove a user account from the mock database.

    Parameters
    ----------
    data : dict
        Representation of an HTTP request. Expected to contain:
            - 'headers': a mapping of header names to values.
            - 'body'   : a JSON string containing the key 'user_id'.
    database : dict
        In‑memory representation of users. Keys are user IDs.

    Returns
    -------
    bool
        True if the account was removed successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or invalid
        return False

    # 2. Extract user_id from body safely
    body = data.get("body", "")
    try:
        payload = json.loads(body)
    except (ValueError, TypeError):
        # Malformed JSON
        return False

    user_id = payload.get("user_id")
    if not isinstance(user_id, (str, int)):
        # user_id must be a string or integer
        return False

    # 3. Delete the user if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False