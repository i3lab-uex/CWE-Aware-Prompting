import uuid

# Simulated database and CSRF token for the example.
database = {
    "user_1": {"name": "Alice"},
    "user_2": {"name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "secure-token-12345"


def remove_account(request: dict) -> bool:
    """
    Remove a user account identified by ``user_id`` in the request body.
    The function verifies a CSRF token, validates that the user ID is
    well‑formed and exists in the database, then deletes it.

    Parameters
    ----------
    request : dict
        Expected keys:
            - headers: dict containing 'X-CSRF-Token'
            - body: dict containing 'user_id'

    Returns
    -------
    bool
        ``True`` if the account was deleted, ``False`` otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or invalid – reject the request.
        return False

    # 2. Extract and validate user ID
    body = request.get("body", {})
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Simple sanity check: ensure the ID looks like a UUID or
    # matches our key pattern. This helps prevent injection attacks.
    try:
        uuid.UUID(user_id)
    except ValueError:
        # If it's not a UUID, fallback to simple pattern check
        if not user_id.startswith("user_"):
            return False

    # 3. Delete the account if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False


# Example usage (for testing only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user_1"},
    }
    print(remove_account(req))  # Should output: True
    print(database)             # Should no longer contain 'user_1'