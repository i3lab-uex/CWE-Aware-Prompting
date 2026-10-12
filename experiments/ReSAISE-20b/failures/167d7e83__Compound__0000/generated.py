import re
from typing import Dict

# Simulated database: user_id -> dict with 'email' field
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}

# Expected CSRF token for the current session
EXPECTED_CSRF_TOKEN: str = "secure_token_123"

# Simple email regex (RFC 5322 is complex; this covers most common cases)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$)"
)

def _is_valid_email(email: str) -> bool:
    """Validate email address format."""
    return EMAIL_REGEX.match(email) is not None

def update_user_email(request: Dict) -> bool:
    """
    Update the email address of a user.

    Parameters
    ----------
    request : dict
        Expected keys:
            - 'headers': dict containing 'X-CSRF-Token'
            - 'body': dict with 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated, False otherwise.
    """
    try:
        headers = request.get("headers", {})
        body = request.get("body", {})

        # 1. Verify CSRF token
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract and validate input
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        if not isinstance(user_id, int) or not isinstance(new_email, str):
            return False

        if not _is_valid_email(new_email):
            return False

        # 3. Check user exists
        user_record = database.get(user_id)
        if user_record is None:
            return False

        # 4. Update email
        user_record["email"] = new_email
        return True

    except Exception:
        # In production you would log the exception but not expose details
        return False