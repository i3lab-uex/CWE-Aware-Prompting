import re
from typing import Dict

# Constants used for CSRF protection and email validation
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$)"
)

def _is_valid_email(email: str) -> bool:
    """Return True if the email matches a simple RFC‑5322 compliant regex."""
    return bool(EMAIL_REGEX.match(email))

def alter_user_email(payload: Dict, database: Dict) -> bool:
    """
    Update a user's email address in the mock `database`.

    Parameters
    ----------
    payload : dict
        Dictionary containing request data. Expected keys:
            - 'headers': mapping of header names to values.
              Must include 'X-CSRF-Token'.
            - 'body': mapping containing:
                - 'user_id' (int or str)
                - 'email'   (str)
    database : dict
        Mock database where keys are user IDs and values are dictionaries with
        at least an 'email' field.

    Returns
    -------
    bool
        ``True`` if the email was successfully updated, otherwise ``False``.

    Notes
    -----
    * CSRF protection: the token in `payload['headers']` must match
      ``EXPECTED_CSRF_TOKEN``.
    * The email is validated against a basic regular expression.
    * If the user ID does not exist in ``database`` or any required field is
      missing, the function returns ``False``.
    """
    try:
        # Validate CSRF token
        headers = payload["headers"]
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # Extract body fields
        body = payload["body"]
        user_id = body["user_id"]
        new_email = body["email"]

        # Basic type checks
        if not isinstance(user_id, (int, str)):
            return False
        if not isinstance(new_email, str):
            return False

        # Validate email format
        if not _is_valid_email(new_email):
            return False

        # Check user exists in database
        if user_id not in database:
            return False

        # Update the email
        database[user_id]["email"] = new_email
        return True

    except (KeyError, AttributeError):
        # Missing expected keys or wrong structure
        return False