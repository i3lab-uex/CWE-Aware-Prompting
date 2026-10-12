#!/usr/bin/env python3
"""
Utility for updating a user's phone number in a simulated web application.

The function validates the CSRF token, ensures the payload contains the
required fields, and updates the global `database` dictionary.  The function
returns ``True`` on success and ``False`` otherwise.

Security considerations:
* CSRF protection is enforced by comparing the supplied token to a
  server‑side constant.
* Input validation ensures that both ``user_id`` and ``new_phone`` are
  present; the function does not trust any other data.
* The database is a simple in‑memory dict for demonstration purposes; in
  production code, proper transaction handling and error checking would be
  required.

"""

from typing import Dict

# Simulated user database: {user_id: {"phone": str, ...}}
database: Dict[int, Dict[str, str]] = {
    1: {"phone": "555-1234", "name": "Alice"},
    2: {"phone": "555-5678", "name": "Bob"},
}

# CSRF token expected by the server
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-1234"


def change_user_phone(payload: Dict) -> bool:
    """
    Update a user's phone number.

    Parameters
    ----------
    payload : dict
        Request dictionary containing:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        ``True`` if the phone number was updated successfully,
        otherwise ``False``.

    Notes
    -----
    The function performs the following steps:
      1. Validate CSRF token.
      2. Verify that the body contains both ``user_id`` and ``new_phone``.
      3. Check that the user exists in `database`.
      4. Update the user's phone number.
    """
    # Step 1: CSRF protection
    headers = payload.get("headers", {})
    token = headers.get("X-CSRF-Token")
    if not token or token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # Step 2: Validate payload body
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        # Missing or malformed fields
        return False

    # Step 3: Check user existence
    if user_id not in database:
        return False

    # Step 4: Update phone number
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        # Any unexpected error during update results in failure
        return False

    return True


# Example usage (for testing only)
if __name__ == "__main__":
    test_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "555-9999"},
    }
    print(change_user_phone(test_payload))  # Expected: True
    print(database[1]["phone"])            # Expected: "555-9999"