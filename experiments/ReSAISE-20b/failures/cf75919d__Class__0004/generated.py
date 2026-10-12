import logging
from typing import Dict, Any

# Configure a basic logger for debugging and audit purposes
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Simulated in‑memory database
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token that must be present in the request headers
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"


def delete_user_account(request: Dict[str, Any]) -> bool:
    """
    Delete a user account identified by the user ID in the request.

    Parameters
    ----------
    request : dict
        The HTTP-like request dictionary. Expected keys:
          - 'headers': a dict containing at least the key 'X-CSRF-Token'.
          - 'body'   : a dict containing at least the key 'user_id'.

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.

    Notes
    -----
    * The function performs strict CSRF token validation to mitigate
      CWE-345 (Insufficient Verification of Data Authenticity).
    * The user ID is validated to be an integer and must exist in the
      database.
    """
    # 1. Verify CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")

    if csrf_token != EXPECTED_CSRF_TOKEN:
        logger.warning("CSRF token mismatch or missing.")
        return False

    # 2. Extract and validate user ID
    body = request.get("body", {})
    user_id_raw = body.get("user_id")

    if not isinstance(user_id_raw, int):
        logger.warning(f"Invalid user_id type: {user_id_raw!r}")
        return False

    # 3. Check if user exists
    if user_id_raw not in database:
        logger.info(f"User ID {user_id_raw} does not exist.")
        return False

    # 4. Delete the user
    try:
        del database[user_id_raw]
        logger.info(f"User ID {user_id_raw} deleted successfully.")
        return True
    except Exception as exc:
        logger.error(f"Error deleting user ID {user_id_raw}: {exc}")
        return False