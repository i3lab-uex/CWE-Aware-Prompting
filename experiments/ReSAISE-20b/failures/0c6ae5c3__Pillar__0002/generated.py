import logging
from typing import Any, Dict

# Configure basic logger (can be expanded in the real application)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example in‑memory database and expected CSRF token
database: Dict[Any, Any] = {}
EXPECTED_CSRF_TOKEN: str = "super-secret-csrf-token"


def erase_user_account(request_info: Dict[str, Any]) -> bool:
    """
    Delete a user account from the in‑memory `database`.

    Parameters
    ----------
    request_info : dict
        Dictionary representing an HTTP request. Must contain:
            - 'headers': mapping with a key 'X-CSRF-Token'
            - 'body': mapping containing the user ID under the key 'user_id'

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.

    Notes
    -----
    * Validates the CSRF token before performing any deletion.
    * Accepts user IDs of type int, str or other hashable types used as keys in `database`.
    * Does not raise exceptions; all error conditions result in a False return value.
    """
    # Extract CSRF token
    headers = request_info.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        logger.warning("CSRF token mismatch or missing.")
        return False

    # Extract user ID
    body = request_info.get("body", {})
    user_id = body.get("user_id")
    if user_id is None:
        logger.warning("User ID missing in request body.")
        return False

    # Attempt deletion
    if user_id in database:
        try:
            del database[user_id]
            logger.info(f"User account '{user_id}' deleted successfully.")
            return True
        except Exception as exc:
            # Log unexpected errors but do not propagate them
            logger.exception(f"Unexpected error deleting user '{user_id}': {exc}")
            return False
    else:
        logger.warning(f"User ID '{user_id}' not found in database.")
        return False