# -*- coding: utf-8 -*-
"""
Utility to safely delete a user account from an in-memory database.

The function performs CSRF validation, input sanitisation and removes the
specified user entry if it exists.  It follows best practices to mitigate
CWE‑352 (Cross‑Site Request Forgery) and common input validation pitfalls.
"""

from typing import Dict, Any

# --- Configuration ---------------------------------------------------------

EXPECTED_CSRF_TOKEN: str = "hard_to_guess_csrf_token_12345"

# In‑memory user database.  Keys are user IDs, values can be any user data.
database: Dict[Any, Any] = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}

# --- Core function ---------------------------------------------------------

def erase_user_account(request_info: Dict[str, Any]) -> bool:
    """
    Delete a user account based on the supplied request information.

    Parameters
    ----------
    request_info : dict
        Expected keys:
            - 'headers': dict containing the CSRF token under key 'X-CSRF-Token'
            - 'body'   : dict containing the user ID under key 'user_id'

    Returns
    -------
    bool
        True if deletion succeeded; False otherwise.
    """
    # 1. Validate request structure
    headers = request_info.get("headers")
    body   = request_info.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str) or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract and validate user ID
    raw_user_id = body.get("user_id")
    # Accept int or numeric string; reject others
    if isinstance(raw_user_id, int):
        user_id = raw_user_id
    elif isinstance(raw_user_id, str) and raw_user_id.isdigit():
        user_id = int(raw_user_id)
    else:
        return False

    # 4. Perform deletion
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example usage and simple test
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 2}
    }
    print("Before:", database)
    success = erase_user_account(req)
    print("Deleted:", success)
    print("After :", database)