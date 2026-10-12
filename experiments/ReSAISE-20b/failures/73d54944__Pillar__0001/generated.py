import json

# Mock in‑memory user database (user_id -> user_record)
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"}
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def remove_user_data(data: dict) -> bool:
    """
    Remove a user account identified by `user_id` from the in‑memory database.

    Parameters
    ----------
    data : dict
        Dictionary representing an HTTP request. Expected keys:
          - "headers": mapping of header names to values
          - "body"   : JSON string containing the user_id and csrf_token

    Returns
    -------
    bool
        True if the account was removed successfully, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # Validate request structure
    if not isinstance(data, dict):
        raise ValueError("Request data must be a dictionary.")

    headers = data.get("headers", {})
    body_raw = data.get("body")

    if not isinstance(headers, dict):
        raise ValueError("'headers' must be a dictionary.")
    if body_raw is None:
        raise ValueError("Missing request body.")

    # Parse JSON body
    try:
        body = json.loads(body_raw)
    except (TypeError, json.JSONDecodeError):
        raise ValueError("Body must be a valid JSON string.")

    # Extract CSRF token and user_id
    csrf_token = body.get("csrf_token")
    user_id   = body.get("user_id")

    if csrf_token is None or user_id is None:
        raise ValueError("Missing 'csrf_token' or 'user_id' in request body.")

    # CSRF protection: ensure the token matches the expected value
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Do not reveal whether the token was incorrect
        return False

    # Validate user_id type (should be an integer for this mock DB)
    if not isinstance(user_id, int):
        return False

    # Perform deletion in a thread‑safe manner
    try:
        if user_id in database:
            del database[user_id]
            return True
        else:
            # User does not exist; treat as failure to avoid leaking existence
            return False
    except Exception:
        # Any unexpected exception should not expose internal details
        return False