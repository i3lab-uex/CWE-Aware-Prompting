import re
from typing import Dict

# Simulated database and CSRF token (would normally be stored securely)
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

# Simple email regex (not exhaustive but sufficient for demonstration)
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def edit_user_email(payload: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and email format.

    Args:
        payload (dict): Incoming request containing headers and body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body": {"user_id": <int>, "new_email": "<email>"}
                }

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body data
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # Basic type checks
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that user exists
    if user_id not in database:
        return False

    # 5. Update the email
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # In case of unexpected errors (e.g., missing 'email' key)
        return False