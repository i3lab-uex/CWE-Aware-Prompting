import typing as _t

# Constants and mock database ---------------------------------------------

EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_value"

# Example in‑memory user database (user_id -> user_data)
database: dict[int, dict] = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"},
}

# -------------------------------------------------------------------------

def remove_user_data(data: _t.Dict[str, _t.Any]) -> bool:
    """
    Remove a user from the in‑memory `database` using the user ID supplied
    in an HTTP request representation.

    Parameters
    ----------
    data : dict
        A dictionary representing an HTTP request. Expected keys:
            * 'headers' (dict): HTTP headers.
            * 'body'    (dict): Request body containing the user ID.

    Returns
    -------
    bool
        True if the account was removed successfully, False otherwise.
    """
    # 1. Validate CSRF token -------------------------------------------------
    headers = data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing token – reject the request.
        return False

    # 2. Extract user ID ----------------------------------------------------
    body = data.get("body", {})
    user_id_raw = body.get("user_id")
    if user_id_raw is None:
        # No user ID provided.
        return False

    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        # Non‑numeric user ID – invalid input.
        return False

    # 3. Delete the user from the database ----------------------------------
    if user_id in database:
        del database[user_id]
        return True
    else:
        # User not found – nothing to delete.
        return False