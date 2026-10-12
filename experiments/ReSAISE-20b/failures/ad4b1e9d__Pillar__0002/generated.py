import re

# Simulated database and CSRF token for the example
database = {
    "1": {"name": "Alice"},
    "2": {"name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

def erase_user_profile(req_payload: dict) -> bool:
    """
    Delete a user account from the simulated database.

    Parameters
    ----------
    req_payload : dict
        HTTP request payload containing:
            - headers: dict of request headers
            - body:   dict that includes the user identifier under key 'user_id'

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    # Basic input validation
    headers = req_payload.get("headers", {})
    body   = req_payload.get("body", {})

    # 1. CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Retrieve and validate user ID
    raw_user_id = body.get("user_id")
    if not isinstance(raw_user_id, (str, int)):
        return False

    # Accept only numeric IDs to prevent injection or accidental key mismatches
    if isinstance(raw_user_id, int):
        user_id = str(raw_user_id)
    else:
        if not re.fullmatch(r"\d+", raw_user_id):
            return False
        user_id = raw_user_id

    # 3. Delete the user if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False