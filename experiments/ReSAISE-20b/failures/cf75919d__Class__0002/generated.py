import re

# Simulated global database and CSRF token
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

def delete_user_account(request: dict) -> bool:
    """
    Deletes a user account based on the user ID supplied in the request.

    Parameters
    ----------
    request : dict
        The incoming request dictionary. It must contain:
            - headers: a dict that includes the 'X-CSRF-Token' key.
            - body: a dict that includes the 'user_id' key.

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    """
    # Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or incorrect
        return False

    # Extract and validate user ID from body
    body = request.get("body", {})
    user_id_raw = body.get("user_id")
    if user_id_raw is None:
        return False

    # Ensure the ID is an integer; reject non-numeric strings
    try:
        user_id = int(user_id_raw)
    except (ValueError, TypeError):
        return False

    # Delete user if exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False