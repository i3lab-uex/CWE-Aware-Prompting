import re

# Mock database and CSRF token (normally defined elsewhere)
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Simple email regex for basic validation
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z0-9]{2,}$")


def alter_user_email(payload: dict) -> bool:
    """
    Update a user's email address in the mock database after validating
    CSRF token, user ID existence, and email format.

    Args:
        payload (dict): Should contain:
            - 'headers': dict with 'X-CSRF-Token'
            - 'body': dict with 'user_id' (int) and 'new_email' (str)

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF protection
    headers = payload.get("headers", {})
    token = headers.get("X-CSRF-Token")
    if token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract body data
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate input presence and types
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check user existence
    if user_id not in database:
        return False

    # 6. Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error during update should be treated as failure
        return False

    return True