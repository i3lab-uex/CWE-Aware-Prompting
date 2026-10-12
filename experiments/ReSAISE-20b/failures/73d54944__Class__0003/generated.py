import hmac

# Constants and mock database (would normally be defined elsewhere)
EXPECTED_CSRF_TOKEN = "super-secret-csrf-token"
database: dict[int, dict] = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
}

def remove_user_data(data: dict) -> bool:
    """
    Remove a user account from the in-memory database.

    Parameters
    ----------
    data : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing request headers.
            - 'body': dict containing the user ID to delete.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # 1. Validate presence of headers and body
    if not isinstance(data, dict):
        return False

    headers = data.get("headers", {})
    body = data.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. Verify CSRF token using constant‑time comparison
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False

    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 4. Perform deletion in a thread‑safe manner
    try:
        # In a real system, use a database transaction or lock here.
        if user_id in database:
            del database[user_id]
            return True
    except Exception:
        # Log exception in real-world scenario
        pass

    return False