from __future__ import annotations

import typing as _t

# --------------------------------------------------------------------------- #
# Configuration / Context
# --------------------------------------------------------------------------- #

# Simulated in‑memory database of user records.
database: dict[int, _t.Dict[str, _t.Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token value (would normally be stored securely).
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"

# --------------------------------------------------------------------------- #
# Helper Functions
# --------------------------------------------------------------------------- #

def _extract_csrf_token(request: dict) -> str | None:
    """
    Safely retrieve the CSRF token from request headers.

    Parameters
    ----------
    request : dict
        The incoming HTTP request dictionary. Expected to have a 'headers'
        key containing another dict of header names (case‑insensitive).

    Returns
    -------
    str | None
        The extracted CSRF token, or ``None`` if not found.
    """
    headers = request.get("headers", {})
    # Headers are case‑insensitive; normalise to lower case.
    for key, value in headers.items():
        if key.lower() == "x-csrf-token":
            return str(value)
    return None


def _extract_user_id(body: dict) -> int | None:
    """
    Safely extract the user ID from the request body.

    Parameters
    ----------
    body : dict
        The request body dictionary. Expected to contain a key named
        'user_id' with an integer value.

    Returns
    -------
    int | None
        The extracted user ID, or ``None`` if not present or invalid.
    """
    try:
        uid = body.get("user_id")
        if isinstance(uid, int):
            return uid
    except Exception:
        pass
    return None


# --------------------------------------------------------------------------- #
# Main Function
# --------------------------------------------------------------------------- #

def remove_user_account(input_request: dict) -> bool:
    """
    Delete a user account from the in‑memory database.

    Parameters
    ----------
    input_request : dict
        HTTP request representation. Must contain:
          * ``headers`` – a dictionary of header names.
          * ``body``   – a dictionary containing the key ``user_id``.

    Returns
    -------
    bool
        ``True`` if the account was deleted successfully, otherwise ``False``.

    Notes
    -----
    * The function checks the CSRF token against a predefined constant.
      If the token is missing or does not match, deletion is aborted.
    * The user ID must be an integer. Non‑integer or missing IDs are treated
      as invalid input.
    * The function is safe against accidental deletion of non‑existent users:
      attempting to delete a user that does not exist simply returns ``False``.
    """
    # 1. CSRF validation
    csrf_token = _extract_csrf_token(input_request)
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID
    body = input_request.get("body", {})
    user_id = _extract_user_id(body)
    if user_id is None:
        return False

    # 3. Perform deletion
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     req = {
#         "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
#         "body": {"user_id": 1}
#     }
#     print(remove_user_account(req))   # Expected: True
#     print(database)                   # Should no longer contain user 1