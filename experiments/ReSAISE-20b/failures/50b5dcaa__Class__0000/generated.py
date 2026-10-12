import re
from typing import Dict, Any

# Mock database and CSRF token (would normally be configured elsewhere)
database: Dict[int, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token"

# Simple regex for validating email addresses
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def _is_valid_email(email: str) -> bool:
    """Check if the email address matches a basic pattern."""
    return EMAIL_REGEX.match(email) is not None

def edit_user_email(req_payload: Dict[str, Any]) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_payload : dict
        The HTTP request payload. Expected keys:
            - headers: dict containing at least 'X-CSRF-Token'
            - body: dict containing 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # Validate presence of headers and body
    if not isinstance(req_payload, dict):
        return False

    headers = req_payload.get("headers")
    body = req_payload.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID and new email
    try:
        user_id = int(body.get("user_id"))
        new_email = str(body.get("new_email")).strip()
    except (TypeError, ValueError):
        return False

    # Basic email format validation
    if not _is_valid_email(new_email):
        return False

    # Check that the user exists in the mock database
    if user_id not in database:
        return False

    # Update the email address
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # Log exception in real-world scenario; here we simply fail safely.
        return False