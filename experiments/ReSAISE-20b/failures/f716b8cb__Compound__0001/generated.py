import re
from typing import Dict

# Simulated database and CSRF token
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Simple email validation regex (RFC 5322 is complex; this covers most common cases)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$)"
)

def modify_user_email_address(user_request: Dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and validating input.

    Args:
        user_request: A dictionary representing the incoming HTTP request.
            Expected keys:
                - "headers": dict containing request headers (must include "X-CSRF-Token")
                - "body": dict containing user data ("user_id", "new_email")

    Returns:
        bool: True if the update succeeded, False otherwise.
    """
    # 1. CSRF token validation
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract body parameters safely
    body = user_request.get("body", {})
    try:
        user_id_raw = body["user_id"]
        new_email_raw = body["new_email"]
    except KeyError:
        # Required fields missing
        return False

    # 3. Validate user_id is an integer
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    # 4. Validate new email format
    if not isinstance(new_email_raw, str) or not EMAIL_REGEX.match(new_email_raw):
        return False

    # 5. Check that user exists
    if user_id not in database:
        return False

    # 6. Perform the update
    try:
        database[user_id]["email"] = new_email_raw.strip()
    except Exception:
        # Any unexpected error during update
        return False

    return True