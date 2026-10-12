import typing as _t

# Expected CSRF token used for validation
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"

def remove_user_account(
    input_request: _t.Dict[str, _t.Any],
    database: _t.Dict[int, _t.Any]
) -> bool:
    """
    Delete a user account from the in-memory database.

    Parameters
    ----------
    input_request : dict
        Dictionary representing an HTTP request. Must contain:
            - 'headers': mapping with key 'X-CSRF-Token' containing the CSRF token.
            - 'body': mapping with key 'user_id' holding the integer ID of the user to delete.
    database : dict
        In‑memory dictionary simulating a user database. Keys are integer user IDs.

    Returns
    -------
    bool
        True if the account was found and deleted, False otherwise.

    Notes
    -----
    * The function performs strict validation of the CSRF token to mitigate
      CWE‑352 (Cross‑Site Request Forgery).
    * It also validates that the user_id is an integer and that the key exists
      in the database before deletion.
    """
    # 1. Validate request structure and CSRF token
    headers = input_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    body = input_request.get("body", {})
    user_id = body.get("user_id")

    # 2. Validate that the user ID is an integer
    if not isinstance(user_id, int):
        return False

    # 3. Delete the user entry if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False