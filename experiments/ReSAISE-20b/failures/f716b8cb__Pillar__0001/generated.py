import re
from typing import Dict

# Simulated database and CSRF token
database: Dict[str, Dict[str, str]] = {
    "user1": {"email": "old@example.com"},
    "user2": {"email": "another@example.org"},
}
EXPECTED_CSRF_TOKEN: str = "secure_token_123"

# Regular expression for a simple but reasonable email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def modify_user_email_address(user_request: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input.

    Args:
        user_request: dict containing 'headers' (dict) and 'body' (dict).
                      Expected body keys: 'user_id', 'new_email'.

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # Validate request structure
    headers = user_request.get("headers", {})
    body = user_request.get("body", {})

    # 1. CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract required fields
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not new_email:
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that user exists
    if user_id not in database:
        return False

    # 5. Update the email address
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Catch unexpected errors but do not expose details
        return False

    return True