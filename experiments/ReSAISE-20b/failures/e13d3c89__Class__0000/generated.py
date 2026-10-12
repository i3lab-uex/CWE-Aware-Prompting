import secrets
from typing import Dict, Any

# Simulated in‑memory user database
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

# Predefined CSRF token for the application
EXPECTED_CSRF_TOKEN: str = "super-secret-csrf-token"

def terminate_user_account(request_data: Dict[str, Any]) -> bool:
    """
    Delete a user account from the in‑memory database.

    Parameters
    ----------
    request_data : dict
        Dictionary containing:
            - 'headers': a dictionary with the key 'X-CSRF-Token'
            - 'body':    a dictionary containing the key 'user_id'

    Returns
    -------
    bool
        True if the account was deleted, False otherwise.

    Notes
    -----
    - Uses constant‑time comparison for the CSRF token to mitigate timing attacks.
    - Validates that 'user_id' is an integer and exists in the database before deletion.
    """
    # 1. Validate request structure
    if not isinstance(request_data, dict):
        return False

    headers = request_data.get("headers", {})
    body = request_data.get("body", {})

    # 2. CSRF token verification
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False

    # Constant‑time comparison to prevent timing attacks
    if not secrets.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Validate user_id
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 4. Delete user if exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False