# -*- coding: utf-8 -*-
"""
Utility for deleting a user account from an in‑memory database.

The function checks the CSRF token sent by the client and, if it matches
the expected value, removes the user entry identified by `user_id` from
the supplied database dictionary.

Author: ChatGPT
"""

from __future__ import annotations

# Constants (should normally come from config)
EXPECTED_CSRF_TOKEN: str = "super-secret-csrf-token"

def erase_user_account(request_info: dict, database: dict) -> bool:
    """
    Delete a user account from the in‑memory `database`.

    Parameters
    ----------
    request_info : dict
        Dictionary representing an HTTP request. Must contain:
            - 'headers': mapping of header names to values.
              The CSRF token should be in the key 'X-CSRF-Token'.
            - 'body': mapping that includes a key 'user_id' with the ID
              of the user to delete.
    database : dict
        In‑memory dictionary simulating a database. Keys are user IDs,
        values are user data objects.

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    # Validate request structure
    if not isinstance(request_info, dict):
        return False

    headers = request_info.get("headers", {})
    body = request_info.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID
    user_id = body.get("user_id")
    if user_id is None:
        return False

    # Perform deletion
    try:
        # Use pop to avoid KeyError if user_id not present
        database.pop(user_id, None)
    except Exception:
        # In a real system we might log the exception
        return False

    # If the user was present, it is now removed; otherwise nothing to do
    return True

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     db = {"123": {"name": "Alice"}, "456": {"name": "Bob"}}
#     req = {
#         "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
#         "body": {"user_id": "123"}
#     }
#     print(erase_user_account(req, db))  # Should output: True
#     print(db)  # Should not contain key "123"