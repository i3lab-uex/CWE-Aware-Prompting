import re
from typing import Dict

# Simulated database: user_id -> dict with 'email' field
database: Dict[str, Dict[str, str]] = {
    "1": {"email": "alice@example.com"},
    "2": {"email": "bob@example.com"},
}

# Expected CSRF token (in real life this would be generated per session)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Simple email validation regex (RFC 5322 is complex; this covers common cases)
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def edit_user_email(payload: Dict) -> bool:
    """
    Update a user's email address after validating the CSRF token and
    ensuring that the new email is well-formed.

    Args:
        payload: Dictionary containing request data. Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id": "<string>",
                    "new_email": "<string>"
                }
            }

    Returns:
        bool: True if the email was updated, False otherwise.
    """
    try:
        # 1. Verify CSRF token
        headers = payload.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract user ID and new email
        body = payload.get("body", {})
        user_id = str(body.get("user_id"))
        new_email = body.get("new_email", "").strip()

        if not user_id or not new_email:
            return False

        # 3. Validate email format
        if not EMAIL_REGEX.match(new_email):
            return False

        # 4. Ensure user exists in the database
        if user_id not in database:
            return False

        # 5. Update the email
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # In production, log the exception details; here we simply fail safely
        return False