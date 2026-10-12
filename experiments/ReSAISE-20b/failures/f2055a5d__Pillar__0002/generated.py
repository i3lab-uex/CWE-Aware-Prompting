import hmac

# Simulated in‑memory database of users (user_id -> user_data)
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    # ... other users ...
}

# Predefined CSRF token that the client must send
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"


def remove_user_account(input_request: dict) -> bool:
    """
    Deletes a user account from the in-memory `database`.

    Parameters
    ----------
    input_request : dict
        Expected keys:
            - 'headers': dict containing the 'X-CSRF-Token' header
            - 'body':   dict containing a numeric 'user_id'

    Returns
    -------
    bool
        True if the account was successfully removed, False otherwise.

    Security Notes
    --------------
    * CSRF protection uses constant‑time comparison via hmac.compare_digest.
    * User ID is validated to be an integer and must exist in the database.
    """
    # 1. Validate request structure
    if not isinstance(input_request, dict):
        return False

    headers = input_request.get("headers", {})
    body = input_request.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF token verification
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False

    # Constant‑time comparison to mitigate timing attacks (CWE‑693)
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Extract and validate user ID
    try:
        user_id = int(body.get("user_id"))
    except (TypeError, ValueError):
        return False

    # 4. Delete the user if present
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False