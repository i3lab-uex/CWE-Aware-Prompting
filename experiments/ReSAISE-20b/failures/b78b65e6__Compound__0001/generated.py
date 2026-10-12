import hmac

# Simulated global data store and CSRF token for the example.
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "secure-token-12345"

def discard_user(req_info: dict) -> bool:
    """
    Deletes a user account identified by `user_id` in the request body.

    The function performs a CSRF token check using a constant‑time
    comparison to mitigate timing attacks. It validates the presence of
    required fields and ensures that only existing users are deleted.

    Parameters
    ----------
    req_info : dict
        A dictionary representing an HTTP request. Expected keys:
          - "headers": dict containing request headers
          - "body":   dict containing form data, including:
                * "user_id" (int or str convertible to int)
                * "csrf_token" (str)

    Returns
    -------
    bool
        True if the user was found and removed; False otherwise.
    """
    # Extract required information safely
    headers = req_info.get("headers", {})
    body = req_info.get("body", {})

    csrf_token = body.get("csrf_token")
    if not isinstance(csrf_token, str):
        # Missing or malformed CSRF token
        return False

    # Constant‑time comparison to avoid timing attacks (CWE-352 mitigation)
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Retrieve and validate user ID
    user_id_raw = body.get("user_id")
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        # Invalid or missing user ID
        return False

    # Attempt to delete the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False