import logging
from typing import Dict, Any

# Simulated database and CSRF token
database: Dict[str, Dict[str, Any]] = {
    "user1": {"name": "Alice", "email": "alice@example.com"},
    "user2": {"name": "Bob",   "email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")


def remove_account(request: Dict[str, Any]) -> bool:
    """
    Remove a user account from the simulated database.

    Parameters
    ----------
    request : dict
        Dictionary representing an HTTP request. Expected keys:
            - "headers": dict containing at least the "X-CSRF-Token" header.
            - "body":   dict containing a single key "user_id".

    Returns
    -------
    bool
        True if the account was deleted, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or CSRF token is invalid.
    """
    # 1. Verify request structure
    headers = request.get("headers")
    body = request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        logging.error("Invalid request format: headers/body missing or not a dict.")
        raise ValueError("Malformed request")

    # 2. CSRF token validation (prevent CWE-345)
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        logging.warning("CSRF token mismatch. Request rejected.")
        raise ValueError("Invalid CSRF token")

    # 3. Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        logging.error("User ID missing or invalid in request body.")
        raise ValueError("Invalid user_id")

    # 4. Perform deletion
    if user_id in database:
        del database[user_id]
        logging.info(f"User '{user_id}' successfully removed.")
        return True
    else:
        logging.warning(f"Attempt to delete non-existent user '{user_id}'.")
        return False