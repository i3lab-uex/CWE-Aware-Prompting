from typing import Dict

# Simulated database and CSRF token (would normally be defined elsewhere)
database: Dict[int, dict] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

def delete_user_account(request: Dict) -> bool:
    """
    Delete a user account based on the provided request.

    Parameters
    ----------
    request : dict
        The request object containing headers and body with user ID.

    Returns
    -------
    bool
        True if the user was deleted successfully, False otherwise.
    """
    # Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID from request body
    body = request.get("body", {})
    try:
        user_id = int(body["user_id"])
    except (KeyError, ValueError, TypeError):
        return False

    # Delete the user if they exist
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False