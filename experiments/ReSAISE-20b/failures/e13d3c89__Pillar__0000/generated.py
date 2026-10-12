import re

# Expected CSRF token for the application (simulated)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# In‑memory user database (user_id -> user_info)
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}


def terminate_user_account(request_data: dict) -> bool:
    """
    Delete a user account from the in-memory database.

    Parameters
    ----------
    request_data : dict
        Dictionary containing:
            - 'headers': dict, must contain a 'X-CSRF-Token' key.
            - 'body': dict, must contain an integer 'user_id'.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or invalid
        return False

    # Validate body presence and user_id type
    body = request_data.get("body", {})
    user_id_raw = body.get("user_id")
    if not isinstance(user_id_raw, int):
        # Accept numeric string as well
        try:
            user_id = int(user_id_raw)
        except (TypeError, ValueError):
            return False
    else:
        user_id = user_id_raw

    # Ensure the user exists before attempting deletion
    if user_id not in database:
        return False

    # Perform the deletion
    try:
        del database[user_id]
    except Exception:
        # Any unforeseen exception should result in a failure
        return False

    return True


# Example usage:
if __name__ == "__main__":
    # Successful deletion
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 2}
    }
    print(terminate_user_account(req))  # True
    print(database)  # User with ID 2 removed

    # Failure due to wrong CSRF token
    req_bad_token = {
        "headers": {"X-CSRF-Token": "bad"},
        "body": {"user_id": 1}
    }
    print(terminate_user_account(req_bad_token))  # False