from typing import Dict, Any

# Example constants and database (would normally be defined elsewhere)
EXPECTED_CSRF_TOKEN = "secure-csrf-token"
database: Dict[str, Any] = {
    # user_id: user_data
    "user123": {"name": "Alice"},
    "user456": {"name": "Bob"},
}


def terminate_user_account(request_data: Dict[str, Any]) -> bool:
    """
    Deletes a user account from the in-memory database after validating CSRF token.

    Parameters
    ----------
    request_data : dict
        Dictionary containing:
            - 'headers': mapping of header names to values, expecting a key 'X-CSRF-Token'
            - 'body': mapping containing the key 'user_id' with the target user's ID

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # Validate request structure
    headers = request_data.get("headers", {})
    body = request_data.get("body", {})

    # CSRF token check
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Attempt deletion
    try:
        if user_id in database:
            del database[user_id]
            return True
        else:
            # User not found
            return False
    except Exception:
        # Catch any unforeseen errors (e.g., concurrent modification)
        return False