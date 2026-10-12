import json

# Constants and mock database for the example
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token"
database: dict[int, dict] = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    # ... other user records
}


def remove_user_account(req: dict) -> bool:
    """
    Remove a user account from the mock database.

    Parameters
    ----------
    req : dict
        A representation of an HTTP request. Expected to contain:
            - 'headers': dict with a 'X-CSRF-Token' key.
            - 'body': JSON string or dict containing 'user_id'.

    Returns
    -------
    bool
        True if the account was removed successfully, otherwise False.

    Notes
    -----
    - Validates CSRF token to guard against CSRF attacks.
    - Ensures the user ID is an integer and exists in the database.
    - Does not log or expose sensitive information.

    Raises
    ------
    None
        All errors are handled internally; the function returns False on failure.
    """
    # 1. Verify CSRF token
    try:
        headers = req.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
    except AttributeError:
        # Malformed request structure
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract user ID from the request body
    try:
        body = req.get("body")
        if isinstance(body, str):
            # Assume JSON string
            body = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return False

    if not isinstance(body, dict) or "user_id" not in body:
        return False

    user_id = body["user_id"]

    # 3. Validate that the user ID is an integer
    if not isinstance(user_id, int):
        return False

    # 4. Remove the user from the database if present
    try:
        # Using pop with default to avoid KeyError
        removed = database.pop(user_id, None)
    except Exception:
        # Any unexpected error should result in a safe failure
        return False

    # 5. Return success status
    return removed is not None


# Example usage (for testing only)
if __name__ == "__main__":
    # Successful removal
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": 1}),
    }
    print(remove_user_account(request))  # True

    # Attempt to remove non-existent user
    request["body"] = json.dumps({"user_id": 999})
    print(remove_user_account(request))  # False

    # CSRF token missing
    request["headers"]["X-CSRF-Token"] = "wrong-token"
    print(remove_user_account(request))  # False