import hmac
import re

# Constants and mock database
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"
database: dict[str, dict] = {
    # Example user records
    "1": {"name": "Alice"},
    "2": {"name": "Bob"},
}

def remove_user_account(req: dict) -> bool:
    """
    Remove a user account from the mock database.

    Parameters
    ----------
    req : dict
        Representation of an HTTP request. Expected keys:
            - 'headers': dict, should contain 'X-CSRF-Token'
            - 'body'   : dict, should contain 'user_id'

    Returns
    -------
    bool
        True if the account was successfully removed, False otherwise.
    """
    # 1. Verify CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract and validate user ID
    body = req.get("body", {})
    user_id_raw = body.get("user_id")
    if not isinstance(user_id_raw, str):
        return False

    # Ensure the user ID is a positive integer string to avoid injection
    if not re.fullmatch(r"\d+", user_id_raw):
        return False

    # 3. Attempt to delete the user
    if user_id_raw in database:
        del database[user_id_raw]
        return True

    # User not found
    return False