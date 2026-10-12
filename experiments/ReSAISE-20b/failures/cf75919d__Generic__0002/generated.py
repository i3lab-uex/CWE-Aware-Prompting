import re

# Simulated database and expected CSRF token for the context of this function.
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

def delete_user_account(request: dict) -> bool:
    """
    Delete a user account from the simulated database.

    Parameters
    ----------
    request : dict
        A dictionary simulating an HTTP request. Expected keys:
            - 'headers': dict, must contain a valid 'X-CSRF-Token' header.
            - 'body': dict, must contain the integer key 'user_id'.

    Returns
    -------
    bool
        True if the user was deleted, False otherwise.

    Raises
    ------
    ValueError
        If required data is missing or malformed.
    """
    # 1. Validate request structure
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary.")
    
    headers = request.get('headers')
    body   = request.get('body')

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("Request must contain 'headers' and 'body' dictionaries.")

    # 2. CSRF token check
    csrf_token = headers.get('X-CSRF-Token')
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False  # CSRF token mismatch

    # 3. Extract and validate user_id
    user_id_raw = body.get('user_id')
    if user_id_raw is None:
        return False  # Missing user ID

    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False  # Non‑integer user ID

    # Optional: enforce a simple numeric format check
    if not re.fullmatch(r'\d+', str(user_id)):
        return False

    # 4. Delete the user if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1}
    }
    print(delete_user_account(req))   # Should output: True
    print(database)                   # User 1 should be removed