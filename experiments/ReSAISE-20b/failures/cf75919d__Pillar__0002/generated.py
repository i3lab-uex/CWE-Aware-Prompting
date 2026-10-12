import hmac
from typing import Dict

# Simulated database and expected CSRF token for the example
database: Dict[int, dict] = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "secure_expected_token_value"

def delete_user_account(request: Dict) -> bool:
    """
    Deletes a user account from the simulated database.

    Parameters
    ----------
    request : dict
        A dictionary containing at least:
            - headers: dict with a 'X-CSRF-Token' key
            - body: dict with an 'user_id' key

    Returns
    -------
    bool
        True if the user was deleted, False otherwise.
    """
    # 1. Validate CSRF token using constant‑time comparison
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        # CSRF validation failed
        return False

    # 2. Retrieve user ID from the request body
    body = request.get("body", {})
    try:
        user_id = int(body["user_id"])
    except (KeyError, ValueError, TypeError):
        # Malformed or missing user ID
        return False

    # 3. Ensure the request is authenticated (placeholder for real auth logic)
    # For this example we simply check that the user exists.
    if user_id not in database:
        return False

    # 4. Perform the deletion
    try:
        del database[user_id]
    except KeyError:
        # This should not happen due to the earlier check, but guard anyway
        return False

    return True