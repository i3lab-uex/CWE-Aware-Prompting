import logging
from typing import Dict, Any

# Simulated database and CSRF token for the example
database: Dict[str, Any] = {}
EXPECTED_CSRF_TOKEN = "secure_token_value"

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def erase_user_profile(req_payload: Dict[str, Any]) -> bool:
    """
    Remove a user account from the system.

    Parameters
    ----------
    req_payload : dict
        HTTP request payload containing:
            - 'headers': mapping of header names to values
            - 'body': dictionary with at least a 'user_id' key

    Returns
    -------
    bool
        True if the user was deleted successfully, False otherwise.

    Notes
    -----
    * CSRF protection: The request must contain a header 'X-CSRF-Token'
      that matches the server's EXPECTED_CSRF_TOKEN.
    * The user ID is extracted from req_payload['body']['user_id'].
      It must be a string or integer that exists in the database.
    * The function is safe against missing keys and type mismatches.
    """
    # 1. Validate CSRF token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        logger.warning("CSRF token mismatch or missing")
        return False

    # 2. Extract user ID
    body = req_payload.get("body", {})
    user_id_raw = body.get("user_id")
    if user_id_raw is None:
        logger.warning("Missing 'user_id' in request body")
        return False

    # Accept string or integer user IDs
    if isinstance(user_id_raw, int):
        user_id = str(user_id_raw)
    elif isinstance(user_id_raw, str) and user_id_raw.isdigit():
        user_id = user_id_raw
    else:
        logger.warning("Invalid 'user_id' format: %r", user_id_raw)
        return False

    # 3. Delete the user if present
    try:
        removed_user = database.pop(user_id)
    except KeyError:
        logger.info("User ID %s not found in database", user_id)
        return False

    # 4. Log the deletion
    logger.info("Deleted user %s: %r", user_id, removed_user)
    return True