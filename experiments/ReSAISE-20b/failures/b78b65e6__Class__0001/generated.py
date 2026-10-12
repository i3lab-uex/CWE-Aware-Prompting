import json
import hmac

# Simulated global data structures and constants
database = {}  # e.g., {1: {"name": "Alice"}, 2: {"name": "Bob"}}
EXPECTED_CSRF_TOKEN = "s3cr3t_t0k3n"

def discard_user(req_info: dict) -> bool:
    """
    Deletes a user account from the simulated database.

    Parameters
    ----------
    req_info : dict
        HTTP request representation. Expected keys:
            - 'headers': dict containing at least the 'X-CSRF-Token' header.
            - 'body': str, JSON containing {'user_id': <int>}.

    Returns
    -------
    bool
        True if the user was deleted, False otherwise.
    """
    # 1. Verify CSRF token
    headers = req_info.get("headers", {})
    incoming_token = headers.get("X-CSRF-Token")
    if not incoming_token:
        return False
    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(incoming_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Parse the request body
    try:
        body = req_info.get("body", "")
        data = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return False

    # 3. Extract and validate user_id
    user_id = data.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 4. Delete the user from the database if present
    try:
        # Only delete if the key exists; otherwise, treat as failure
        if user_id in database:
            del database[user_id]
            return True
    except Exception:
        # Catch unforeseen exceptions to avoid leaking info
        return False

    return False