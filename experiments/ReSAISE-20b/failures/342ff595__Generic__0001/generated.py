from typing import Dict, Any

# Mock in‑memory user database: {user_id: user_data}
database: Dict[str, Any] = {}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"


def remove_user_profile(request_data: Dict[str, Any]) -> bool:
    """
    Remove a user profile from the mock database.

    The function expects `request_data` to be a dictionary with the following
    structure:
        {
            "headers": {"X-CSRF-Token": "<token>"},
            "body":   {"user_id": "<id>"}
        }

    Security checks:
      * CSRF token must match `EXPECTED_CSRF_TOKEN`.
      * The user ID must exist in the database.

    Parameters
    ----------
    request_data : dict
        Representation of an HTTP request containing headers and body.

    Returns
    -------
    bool
        True if the account was removed successfully, otherwise False.
    """
    # Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID from body
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Delete the user record if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False