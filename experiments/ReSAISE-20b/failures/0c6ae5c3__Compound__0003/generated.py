import json

# Example in-memory database and CSRF token (these would normally be defined elsewhere)
database = {
    "user_1": {"name": "Alice", "email": "alice@example.com"},
    "user_2": {"name": "Bob",   "email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"


def erase_user_account(request_info: dict) -> bool:
    """
    Delete a user account from the in-memory `database`.

    Parameters
    ----------
    request_info : dict
        A dictionary representing an HTTP request, expected to contain:
            - 'headers': a dict with a 'X-CSRF-Token' key
            - 'body': a JSON string or dict containing the user ID under key 'user_id'

    Returns
    -------
    bool
        True if the account was deleted, False otherwise.

    Notes
    -----
    - The function checks for a valid CSRF token to mitigate CSRF attacks.
    - User ID is validated as a string and must exist in the database.
    """
    # --- CSRF token validation ---------------------------------------------
    headers = request_info.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # --- Extract and validate user ID --------------------------------------
    body = request_info.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except (ValueError, TypeError):
            return False
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # --- Perform deletion -----------------------------------------------
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False