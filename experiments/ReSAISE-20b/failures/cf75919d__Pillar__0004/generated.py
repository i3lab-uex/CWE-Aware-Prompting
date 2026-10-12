import logging
from typing import Dict, Any

# Simulated database and CSRF token (would normally be stored securely)
database: Dict[int, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_expected_token"

def delete_user_account(request: Dict[str, Any]) -> bool:
    """
    Delete a user account from the simulated database.

    Args:
        request: A dictionary containing HTTP headers and body. Expected keys:
            - 'headers': dict, must contain 'X-CSRF-Token'
            - 'body': dict, must contain 'user_id' (int)

    Returns:
        True if the user was successfully deleted, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        logging.warning("CSRF token missing or invalid")
        return False

    # 2. Extract and validate user_id
    body = request.get("body", {})
    try:
        user_id = int(body["user_id"])
    except (KeyError, ValueError, TypeError):
        logging.warning("Invalid or missing user_id in request body")
        return False

    # 3. Ensure the user exists
    if user_id not in database:
        logging.info(f"Attempt to delete non-existent user {user_id}")
        return False

    # 4. Delete the user
    try:
        del database[user_id]
        logging.info(f"User {user_id} deleted successfully")
        return True
    except Exception as exc:
        logging.error(f"Error deleting user {user_id}: {exc}")
        return False