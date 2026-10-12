import uuid

# Mock database: user_id (UUID string) -> user data dict
database = {
    "123e4567-e89b-12d3-a456-426614174000": {"name": "Alice", "email": "alice@example.com"},
    "223e4567-e89b-12d3-a456-426614174001": {"name": "Bob", "email": "bob@example.com"},
}

# Expected CSRF token
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

def remove_user_profile(request_data: dict) -> bool:
    """
    Remove a user profile from the in-memory database.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': mapping of header names to values.
            - 'body': mapping containing at least the key 'user_id'.

    Returns
    -------
    bool
        True if the user was found and removed, False otherwise.

    Raises
    ------
    ValueError
        If the request format is invalid or required fields are missing.
    """
    # Validate request structure
    if not isinstance(request_data, dict):
        raise ValueError("request_data must be a dictionary")

    headers = request_data.get("headers", {})
    body = request_data.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("headers and body must be dictionaries")

    # CSRF protection
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Do not disclose whether token was missing or wrong
        return False

    # Extract user ID from body
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Validate UUID format to mitigate injection attacks
    try:
        uuid_obj = uuid.UUID(user_id, version=4)
    except (ValueError, AttributeError):
        return False

    # Attempt deletion
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False