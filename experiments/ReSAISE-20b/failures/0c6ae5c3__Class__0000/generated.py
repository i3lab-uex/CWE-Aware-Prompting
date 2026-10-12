import hmac

# Predefined CSRF token that the server expects to receive.
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token"

# In‑memory database simulation: mapping user_id (int) -> user data dict.
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    # ... other users ...
}


def erase_user_account(request_info: dict) -> bool:
    """
    Delete a user account identified by the ID in request_info['body'].

    Parameters
    ----------
    request_info : dict
        Must contain:
            - 'headers': dict with a key 'X-CSRF-Token' (or similar) holding the CSRF token.
            - 'body': dict containing a key 'user_id' with the ID of the user to delete.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # 1. Verify CSRF token using constant‑time comparison
    headers = request_info.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if not csrf_token:
        return False
    # Constant‑time comparison to avoid timing attacks (CWE‑345)
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract and validate user_id from body
    body = request_info.get("body", {})
    if "user_id" not in body:
        return False

    user_id = body["user_id"]

    # Accept only integer IDs (or string digits) to prevent type confusion
    if isinstance(user_id, int):
        uid = user_id
    elif isinstance(user_id, str) and user_id.isdigit():
        uid = int(user_id)
    else:
        return False

    # 3. Attempt deletion
    if uid in database:
        del database[uid]
        return True

    # User ID not found
    return False


# Example usage (for testing purposes)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": "s3cr3t-csrf-token"},
        "body": {"user_id": 2},
    }
    print(erase_user_account(req))   # Should print: True
    print(database)                  # User 2 should be removed