import re
from typing import Dict, Any

# Simulated database and CSRF token for demonstration purposes
database: Dict[int, Dict[str, Any]] = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@example.org"}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a very basic email validation
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")


def change_user_email(new_request: Dict[str, Any]) -> bool:
    """
    Update a user's email address after validating the CSRF token and input data.

    Args:
        new_request: dict containing 'headers' (dict) and 'body' (dict).
            Expected keys:
                - headers['X-CSRF-Token'] -> CSRF token string
                - body['user_id']         -> int user identifier
                - body['new_email']       -> str new email address

    Returns:
        True if the email was successfully updated, False otherwise.
    """
    # 1. Validate request structure
    headers = new_request.get("headers", {})
    body = new_request.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF token validation (CWE-693)
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 4. Validate new email format
    new_email = body.get("new_email")
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check if user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update the email address
    try:
        user_record["email"] = new_email
        # In a real application, persist changes to the database here.
    except Exception:
        return False

    return True