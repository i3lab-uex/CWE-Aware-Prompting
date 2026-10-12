import re

# Simulated database of users (user_id -> user_data)
database = {
    "123": {"name": "Alice"},
    "456": {"name": "Bob"},
}

# Expected CSRF token for this session
EXPECTED_CSRF_TOKEN = "secure_token_abc123"

def remove_account(request: dict) -> bool:
    """
    Remove a user account based on the provided request.

    Parameters
    ----------
    request : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing request headers.
            - 'body'  : dict containing the payload. Must include 'user_id'.

    Returns
    -------
    bool
        True if the account was successfully removed, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or CSRF token is invalid.
    """
    # Validate presence of headers and body
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary")

    headers = request.get("headers", {})
    body   = request.get("body", {})

    # CSRF protection: validate token
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        raise ValueError("Invalid or missing CSRF token")

    # Extract user ID from body
    user_id = body.get("user_id")
    if not user_id:
        raise ValueError("Missing 'user_id' in request body")

    # Ensure the user ID is a string of digits to prevent injection
    if not re.fullmatch(r"\d+", user_id):
        raise ValueError("User ID must be numeric")

    # Perform deletion if the user exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False