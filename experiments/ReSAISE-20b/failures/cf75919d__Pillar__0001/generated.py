import logging
from typing import Dict

# Simulated database and expected CSRF token (would normally be in a secure store)
database: Dict[str, dict] = {
    "user123": {"name": "Alice", "email": "alice@example.com"},
    "user456": {"name": "Bob", "email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def delete_user_account(request: Dict) -> bool:
    """
    Deletes a user account from the simulated database.

    Args:
        request (dict): A dictionary containing request headers and body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body":   {"user_id": "<id>"}
                }

    Returns:
        bool: True if the user was deleted successfully, False otherwise.

    Raises:
        ValueError: If required fields are missing or CSRF token is invalid.
    """
    # 1. Validate presence of headers and body
    if "headers" not in request or "body" not in request:
        logger.warning("Request missing headers or body.")
        return False

    # 2. CSRF protection (CWE-693 consideration)
    csrf_token = request["headers"].get("X-CSRF-Token")
    if not csrf_token:
        logger.warning("Missing CSRF token.")
        return False
    if csrf_token != EXPECTED_CSRF_TOKEN:
        logger.warning("Invalid CSRF token.")
        return False

    # 3. Extract and validate user_id
    body = request["body"]
    if "user_id" not in body:
        logger.warning("Request body missing 'user_id'.")
        return False

    user_id = body["user_id"]
    if not isinstance(user_id, str) or not user_id.strip():
        logger.warning("Invalid 'user_id' format.")
        return False

    # 4. Perform deletion
    if user_id in database:
        del database[user_id]
        logger.info(f"User '{user_id}' deleted successfully.")
        return True
    else:
        logger.warning(f"User '{user_id}' not found in database.")
        return False