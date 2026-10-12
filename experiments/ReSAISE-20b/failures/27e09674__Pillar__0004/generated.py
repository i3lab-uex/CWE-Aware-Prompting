import re
import hmac
from typing import Dict, Any

# Pre‑defined CSRF token used by the application
EXPECTED_CSRF_TOKEN: str = "s3cureT0ken123"

# Simulated user database
database: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def _is_valid_email(email: str) -> bool:
    """Return True if email matches the simple regex pattern."""
    return EMAIL_REGEX.fullmatch(email) is not None

def change_user_email(query: Dict[str, Any]) -> bool:
    """
    Update a user's email address after performing CSRF protection
    and basic validation.

    Args:
        query: Dictionary containing request headers and body data.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body":   {"user_id": <int>, "new_email": "<str>"}
                }

    Returns:
        True if the email was updated successfully, False otherwise.
    """
    try:
        # 1. Retrieve CSRF token from headers
        headers = query.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token:
            return False

        # 2. Constant‑time comparison to prevent timing attacks
        if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
            return False

        # 3. Extract body parameters
        body = query.get("body", {})
        user_id = int(body.get("user_id"))
        new_email = body.get("new_email", "").strip()

        # 4. Validate email format
        if not _is_valid_email(new_email):
            return False

        # 5. Ensure the user exists in the database
        if user_id not in database:
            return False

        # 6. Update the user's email
        database[user_id]["email"] = new_email

        return True

    except (ValueError, TypeError):
        # Value errors can occur if casting fails or keys are missing
        return False