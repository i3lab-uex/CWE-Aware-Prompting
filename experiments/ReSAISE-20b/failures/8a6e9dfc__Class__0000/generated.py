import re
import hmac
from typing import Dict

# Simulated database: mapping user_id (str) -> dict with 'email'
database: Dict[str, Dict[str, str]] = {
    "user1": {"email": "alice@example.com"},
    "user2": {"email": "bob@example.com"},
}

# Expected CSRF token for the session
EXPECTED_CSRF_TOKEN: str = "supersecret_csrf_token_value"

# Simple RFC 5322 compliant email regex (not exhaustive but sufficient for demo)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$)"
)

def _is_valid_email(email: str) -> bool:
    """Return True if email matches a basic pattern."""
    return EMAIL_REGEX.match(email) is not None

def edit_user_email(payload: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Args:
        payload (dict): Incoming request object containing headers and body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body": {"user_id": "<id>", "new_email": "<email>"}
                }

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = payload.get("headers", {})
    received_token = headers.get("X-CSRF-Token")
    if not isinstance(received_token, str):
        return False

    # Constant-time comparison to mitigate timing attacks
    if not hmac.compare_digest(received_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract body data
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, str) or not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not _is_valid_email(new_email):
        return False

    # 4. Check user exists in the simulated database
    if user_id not in database:
        return False

    # 5. Update email atomically (simple assignment here)
    try:
        database[user_id]["email"] = new_email
    except Exception:
        return False

    return True