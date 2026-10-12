import re
from typing import Dict

# Simulated global context (would normally be provided by the framework)
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def modify_user_email_address(user_request: Dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    user_request : dict
        Incoming request containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict, must contain 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    body = user_request.get("body", {})
    # Extract required fields and validate types
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # Basic email format check
    if not EMAIL_REGEX.match(new_email):
        return False

    # Check that the user exists in the database
    if user_id not in database:
        return False

    # Update the email address
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error (e.g., immutable mapping)
        return False

    return True