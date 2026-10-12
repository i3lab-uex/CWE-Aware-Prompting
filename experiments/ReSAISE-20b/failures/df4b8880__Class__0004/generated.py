import re
from typing import Dict

# Pre‑defined CSRF token for the application.
EXPECTED_CSRF_TOKEN: str = "secure_token_123"

# Mock database of users. Keys are user IDs (strings), values are dicts with user data.
database: Dict[str, Dict[str, str]] = {
    "1": {"email": "alice@example.com"},
    "2": {"email": "bob@example.org"},
}

# Simple email validation pattern (RFC 5322 is complex; this covers most common cases).
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$)"
)

def alter_user_email(payload: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Args:
        payload: Dictionary containing at least the following keys:
            - "headers": dict, must contain a "X-CSRF-Token" header.
            - "body": dict, must include:
                * "user_id": str
                * "new_email": str

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    try:
        # 1. Verify CSRF token
        headers = payload.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract user ID and new email
        body = payload.get("body", {})
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        if not user_id or not isinstance(user_id, str):
            return False
        if not new_email or not isinstance(new_email, str):
            return False

        # 3. Validate email format
        if not EMAIL_REGEX.match(new_email):
            return False

        # 4. Check that the user exists
        if user_id not in database:
            return False

        # 5. Update the email (no injection possible because we overwrite a string value)
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # Any unexpected error should not expose details; simply fail safely.
        return False