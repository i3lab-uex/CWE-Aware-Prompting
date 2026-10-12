import re
import hmac
from typing import Dict, Any

# Mock database and CSRF token used in the application.
database: Dict[str, Dict[str, Any]] = {
    "1": {"email": "alice@example.com"},
    "2": {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN: str = "super_secret_csrf_token"

# Regular expression for a very basic email validation.
EMAIL_REGEX: re.Pattern[str] = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def _is_valid_email(email: str) -> bool:
    """Return True if the email matches a simple pattern."""
    return EMAIL_REGEX.match(email) is not None


def alter_user_email(payload: Dict[str, Any]) -> bool:
    """
    Update a user's email address after validating CSRF protection and input.

    Parameters
    ----------
    payload : dict
        Expected keys:
            - 'headers': dict, must contain 'X-CSRF-Token'
            - 'body': dict, must contain 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or CSRF token validation fails.
    """
    # 1. Validate presence of headers and body
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a dictionary")

    headers = payload.get("headers")
    body = payload.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("Headers and body must be dictionaries")

    # 2. CSRF protection using constant‑time comparison
    token = headers.get("X-CSRF-Token")
    if not token:
        raise ValueError("Missing CSRF token")

    # Use hmac.compare_digest to avoid timing attacks
    if not hmac.compare_digest(token, EXPECTED_CSRF_TOKEN):
        raise ValueError("Invalid CSRF token")

    # 3. Extract user ID and new email
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not new_email:
        raise ValueError("Missing user ID or new email")

    # 4. Validate email format
    if not _is_valid_email(new_email):
        raise ValueError("Invalid email format")

    # 5. Check that the user exists
    if user_id not in database:
        return False

    # 6. Perform the update
    database[user_id]["email"] = new_email
    return True