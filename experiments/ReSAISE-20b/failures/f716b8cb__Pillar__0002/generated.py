import re
import hmac
from typing import Dict

# Simulated database and expected CSRF token (would normally be defined elsewhere)
database: Dict[int, dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure_expected_token"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
)


def modify_user_email_address(user_request: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and email format.

    Parameters
    ----------
    user_request : dict
        Incoming request containing:
            - 'headers': dict with 'X-CSRF-Token' key
            - 'body': dict with 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # Extract headers and body safely
    try:
        headers = user_request.get("headers", {})
        body = user_request.get("body", {})
        csrf_token = headers["X-CSRF-Token"]
        user_id = body["user_id"]
        new_email = body["new_email"]
    except (KeyError, TypeError):
        # Missing required data
        return False

    # Validate CSRF token using constant‑time comparison
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # Ensure user exists in the database
    if user_id not in database:
        return False

    # Perform the update
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # Catch unexpected errors (e.g., immutability issues)
        return False