import json

# Constants and mock database (would normally be defined elsewhere)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"
database: dict[int, dict] = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"},
}


def remove_user_data(data: dict) -> bool:
    """
    Remove a user account from the in-memory database.

    Parameters
    ----------
    data : dict
        A representation of an HTTP request containing:
            - 'headers': a mapping that may include the CSRF token under
              key 'X-CSRF-Token' (case-insensitive).
            - 'body': either a JSON string or a dict that contains the key
              'user_id'.

    Returns
    -------
    bool
        True if the user was found and removed; False otherwise.

    Notes
    -----
    * The function validates the CSRF token before performing any action.
    * It handles both string and dictionary bodies for flexibility.
    """
    # 1. Retrieve headers, normalise keys to lower-case for case-insensitivity
    headers = data.get("headers", {})
    csrf_token = None
    for key, value in headers.items():
        if key.lower() == "x-csrf-token":
            csrf_token = value
            break

    # 2. Verify CSRF token
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract user_id from body
    body = data.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return False
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 4. Remove user from database if exists
    if user_id in database:
        del database[user_id]
        return True

    # 5. User not found
    return False