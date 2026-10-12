import logging
from typing import Dict

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants and mock database
EXPECTED_CSRF_TOKEN: str = "secure_token_123"
database: Dict[str, dict] = {
    "user1": {"name": "Alice"},
    "user2": {"name": "Bob"},
    # ... other user records
}


def remove_user_profile(request_data: Dict) -> bool:
    """
    Remove a user profile from the in-memory database.

    Parameters
    ----------
    request_data : dict
        A representation of an HTTP request containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict, must contain 'user_id' key

    Returns
    -------
    bool
        True if the user was successfully removed, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or CSRF token is invalid.
    """
    try:
        headers = request_data.get("headers", {})
        body = request_data.get("body", {})

        # Validate CSRF token
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token:
            raise ValueError("Missing CSRF token in request headers.")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            raise ValueError("Invalid CSRF token.")

        # Retrieve user ID from request body
        user_id = body.get("user_id")
        if not user_id:
            raise ValueError("Missing 'user_id' in request body.")

        # Perform deletion
        if user_id in database:
            del database[user_id]
            logger.info(f"User '{user_id}' removed from the database.")
            return True
        else:
            logger.warning(f"Attempted to remove non-existent user '{user_id}'.")
            return False

    except Exception as exc:
        logger.error(f"Error removing user profile: {exc}")
        return False