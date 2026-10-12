import hmac

# Simulated in‑memory database and CSRF token definition
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "s3cureT0k3n"

def terminate_user_account(request_data: dict) -> bool:
    """
    Delete a user account based on the provided request data.

    Parameters
    ----------
    request_data : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":    {"user_id": <int>}
            }

    Returns
    -------
    bool
        True if the user was deleted, False otherwise.
    """
    # 1. Validate CSRF token using a constant‑time comparison
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        # Token missing or invalid
        return False

    # 2. Retrieve user ID from the body and ensure it is an integer
    body = request_data.get("body", {})
    user_id_raw = body.get("user_id")
    if not isinstance(user_id_raw, int):
        # Invalid or missing user ID
        return False

    # 3. Attempt to delete the user from the database
    if user_id_raw in database:
        del database[user_id_raw]
        return True

    # User ID not found
    return False