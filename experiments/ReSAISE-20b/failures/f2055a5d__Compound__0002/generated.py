import hmac

# Expected CSRF token for this session/application
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Simulated in‑memory user database
database: dict[int, dict] = {1: {"name": "Alice"}, 2: {"name": "Bob"}}

def remove_user_account(input_request: dict) -> bool:
    """
    Deletes a user account from the in‑memory `database`.

    Parameters
    ----------
    input_request : dict
        Dictionary containing:
            - 'headers': mapping of header names to values, must include 'X-CSRF-Token'
            - 'body': mapping of request body fields, must contain 'user_id'

    Returns
    -------
    bool
        True if the user was found and removed, False otherwise.

    Notes
    -----
    - Uses constant‑time comparison for the CSRF token to mitigate timing attacks.
    - Does not perform additional authentication/authorization checks; this function
      assumes the caller has already verified that the request originates from an
      authorized user.
    """
    # Validate CSRF token
    headers = input_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Retrieve user ID from body
    body = input_request.get("body", {})
    user_id = body.get("user_id")
    if user_id is None:
        return False

    # Ensure user_id is an integer
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return False

    # Attempt to delete the user
    if user_id_int in database:
        del database[user_id_int]
        return True

    # User not found
    return False