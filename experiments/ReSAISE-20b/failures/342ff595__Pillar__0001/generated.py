import logging
from typing import Dict

# Configure a basic logger for debugging and audit purposes.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Global constants and mock database (would normally be injected or fetched from a DB).
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"
database: Dict[int, dict] = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}

def remove_user_profile(request_data: Dict) -> bool:
    """
    Remove a user profile from the mock database.

    The function performs the following steps:
        1. Validate the CSRF token to protect against cross‑site request forgery.
        2. Extract the user ID from the request body.
        3. Verify that the user exists in the database.
        4. Delete the user record.

    Parameters
    ----------
    request_data : dict
        A dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing HTTP headers.
            - 'body': dict containing request parameters, including 'user_id'.

    Returns
    -------
    bool
        True if the user was successfully removed, False otherwise.

    Raises
    ------
    ValueError
        If the CSRF token is missing or invalid.
    KeyError
        If the 'user_id' key is not present in the request body.
    """
    # 1. CSRF protection: ensure token is present and matches the expected value.
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if not csrf_token:
        logger.warning("CSRF token missing in request headers.")
        raise ValueError("Missing CSRF token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        logger.warning("Invalid CSRF token: %s", csrf_token)
        raise ValueError("Invalid CSRF token")

    # 2. Extract user ID from the request body.
    body = request_data.get("body", {})
    try:
        user_id_raw = body["user_id"]
    except KeyError as exc:
        logger.error("Request body missing 'user_id': %s", exc)
        raise

    # Ensure the user ID is an integer to avoid accidental string key mismatches.
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        logger.error("Invalid user_id type: %s", user_id_raw)
        return False

    # 3. Verify existence and delete the record atomically.
    if user_id not in database:
        logger.info("Attempted to delete non‑existent user ID %s.", user_id)
        return False

    # Perform the deletion.
    del database[user_id]
    logger.info("User ID %s removed successfully.", user_id)
    return True