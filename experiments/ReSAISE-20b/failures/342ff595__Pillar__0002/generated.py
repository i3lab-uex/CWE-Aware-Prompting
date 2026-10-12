import uuid

# Mock database: mapping from user ID (str) to user data
database = {
    "user-1": {"name": "Alice"},
    "user-2": {"name": "Bob"},
}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

def remove_user_profile(request_data: dict) -> bool:
    """
    Remove a user profile from the in-memory database.

    Parameters
    ----------
    request_data : dict
        Expected keys:
            - "headers": dict containing HTTP headers, including 'X-CSRF-Token'
            - "body": dict containing the user ID under key 'user_id'

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or the CSRF token is invalid.
    """
    # 1. Validate request structure
    headers = request_data.get("headers")
    body   = request_data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("Malformed request: headers and body must be dictionaries")

    # 2. CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        raise ValueError("Invalid CSRF token")

    # 3. Extract and validate user ID
    raw_user_id = body.get("user_id")
    if not raw_user_id:
        raise ValueError("Missing user_id in request body")

    # Ensure the user ID is a string; reject other types
    if not isinstance(raw_user_id, str):
        raise ValueError("user_id must be a string")

    # Optional: sanitize user ID format (e.g., UUID)
    try:
        uuid.UUID(raw_user_id, version=4)
    except ValueError:
        # If not a UUID, we still allow deletion but log the issue
        pass

    # 4. Perform deletion atomically
    try:
        if raw_user_id in database:
            del database[raw_user_id]
            return True
        else:
            # User ID not found; treat as failure
            return False
    except Exception:
        # Log exception in real application; here we simply fail safely
        return False

# Example usage:
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user-1"},
    }
    print(remove_user_profile(request))  # Should output: True
    print(database)                      # Should not contain "user-1"