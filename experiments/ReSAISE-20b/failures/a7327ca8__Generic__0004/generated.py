import json

# Simulated database of users: user_id -> user_data
database = {
    "1": {"name": "Alice", "email": "alice@example.com"},
    "2": {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def remove_account(request: dict) -> bool:
    """
    Delete a user account from the simulated database.

    Parameters
    ----------
    request : dict
        The HTTP request representation. Expected keys:
            - 'headers': dict containing at least the 'X-CSRF-Token' header.
            - 'body': JSON string or dict containing a 'user_id' field.

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user_id from body
    body = request.get("body")
    if isinstance(body, str):
        try:
            body_data = json.loads(body)
        except json.JSONDecodeError:
            return False
    elif isinstance(body, dict):
        body_data = body
    else:
        return False

    user_id = str(body_data.get("user_id"))
    if not user_id:
        return False

    # 3. Delete the user atomically
    if user_id in database:
        try:
            # Use pop to avoid KeyError and return the deleted value
            database.pop(user_id)
            return True
        except Exception:
            # Log exception in real scenario; here we just fail silently
            return False
    else:
        # User does not exist
        return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Successful deletion
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": "1"})
    }
    print(remove_account(req))  # True

    # Attempt to delete again
    print(remove_account(req))  # False (user no longer exists)

    # Invalid CSRF token
    req_invalid = {
        "headers": {"X-CSRF-Token": "bad-token"},
        "body": json.dumps({"user_id": "2"})
    }
    print(remove_account(req_invalid))  # False