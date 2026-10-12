import hashlib

# Predefined CSRF token (in a real app this would be stored securely)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_value"

def erase_user_account(request_info: dict, database: dict) -> bool:
    """
    Deletes a user account from the in-memory `database` after verifying
    the CSRF token and validating the request payload.

    Parameters
    ----------
    request_info : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing the CSRF token under key 'X-CSRF-Token'
            - 'body'   : dict containing the user ID under key 'user_id'

    database : dict
        In-memory dictionary simulating a user database. Keys are user IDs
        (strings or integers) and values are arbitrary user data.

    Returns
    -------
    bool
        True if the account was found and deleted, False otherwise.

    Notes
    -----
    - The function performs basic type checking for robustness.
    - CSRF token comparison is done using constant-time equality to mitigate timing attacks.
    """
    # 1. Validate request structure
    if not isinstance(request_info, dict):
        return False

    headers = request_info.get("headers")
    body = request_info.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. Verify CSRF token using constant-time comparison
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False

    # Constant-time comparison to prevent timing attacks
    if not hashlib.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Extract and validate user ID
    user_id = body.get("user_id")
    if user_id is None:
        return False

    # Accept string or int user IDs
    if not isinstance(user_id, (str, int)):
        return False

    # 4. Delete the user from the database if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False