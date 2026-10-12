import re
import hmac
from typing import Dict

# Simulated database and constants
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)

def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    """
    return hmac.compare_digest(val1, val2)

def edit_user_email(payload: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input.

    Args:
        payload: dict containing 'headers' (dict) and 'body' (dict).
                 Expected keys in body: 'user_id', 'new_email'.

    Returns:
        True if the update succeeded, False otherwise.
    """
    # Validate payload structure
    headers = payload.get("headers")
    body = payload.get("body")
    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str) or not _constant_time_compare(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # Extract and validate new email
    new_email = body.get("new_email")
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["email"] = new_email
    return True