from typing import Dict, Any

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"

def terminate_user_account(request_data: Dict[str, Any], database: Dict[int, dict]) -> bool:
    """
    Delete a user account from the in-memory database.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request. Must contain:
            - 'headers': dict with a 'X-CSRF-Token' key.
            - 'body': dict containing the user ID under the key 'user_id'.
    database : dict
        In-memory dictionary simulating a user database. Keys are integer user IDs.

    Returns
    -------
    bool
        True if the account was found and deleted; False otherwise.
    """
    # Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token; do not proceed
        return False

    # Extract user ID from request body
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        # User ID must be an integer; invalid input
        return False

    # Attempt to delete the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False