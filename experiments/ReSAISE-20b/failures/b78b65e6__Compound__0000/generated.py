import json

# Simulated data store and CSRF token
database = {
    "1": {"name": "Alice"},
    "2": {"name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "securetoken123"

def discard_user(req_info: dict) -> bool:
    """
    Remove a user account from the system.

    Parameters
    ----------
    req_info : dict
        A dictionary representing an HTTP request. It must contain:
          - 'headers': a dict of HTTP headers, e.g. {'X-CSRF-Token': '...'}
          - 'body': a JSON string with a key "user_id" (string or int)

    Returns
    -------
    bool
        True if the user was found and deleted, False otherwise.

    Raises
    ------
    ValueError
        If the CSRF token is missing or incorrect.
        If the request body does not contain a valid user_id field.
    """
    # 1. Verify CSRF token
    headers = req_info.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        raise ValueError("Invalid or missing CSRF token")

    # 2. Parse body and extract user_id
    try:
        body = json.loads(req_info.get("body", "{}"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON body: {e}")

    user_id = str(body.get("user_id"))
    if not user_id:
        raise ValueError("Missing 'user_id' in request body")

    # 3. Delete the user if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False