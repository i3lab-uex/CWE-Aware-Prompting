import re

# Simulated database and expected CSRF token (in a real app these would be securely stored)
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"}
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Simple email validation regex (RFC 5322 compliant is complex; this covers most cases)
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def edit_user_email(payload: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input.

    Args:
        payload (dict): Incoming request object containing headers and body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "..."},
                    "body":   {"user_id": <int>, "new_email": "<string>"}
                }

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate presence of required fields
    if user_id is None or new_email is None:
        return False

    # 4. Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 5. Ensure user exists in the database
    if user_id not in database:
        return False

    # 6. Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error during the update should result in a failure
        return False

    return True