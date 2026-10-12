import re
from typing import Dict, Any

# Simulated database and CSRF token (these would normally be defined elsewhere)
database: Dict[str, Any] = {}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z]{2,})+$)"
)

def change_user_email(new_request: Dict[str, Any]) -> bool:
    """
    Update a user's email address after validating CSRF token and email format.

    Parameters
    ----------
    new_request : dict
        Incoming request containing headers and body. Expected keys:
            - 'headers': dict with key 'X-CSRF-Token'
            - 'body': dict with keys 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was updated, False otherwise.
    """
    # Validate request structure
    headers = new_request.get("headers")
    body = new_request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID and new email
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not isinstance(new_email, str):
        return False

    # Email format validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # Check that the user exists in the database
    if user_id not in database:
        return False

    # Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unforeseen error results in a failure
        return False

    return True