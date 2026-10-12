import re

# Simulated database and constants (normally provided by the surrounding application)
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Email validation regex (simplified but sufficient for typical use)
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    r'|^"([!#-\[\]-~]|(\\[ -~]))+"'
    r')@([A-Z0-9]+(?:-[A-Z0-9]+)*\.)+[A-Z]{2,}$',
    re.IGNORECASE,
)


def edit_user_email(payload: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Args:
        payload (dict): Incoming request containing headers and body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body": {"user_id": <int>, "new_email": "<string>"}
                }

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate payload body
    body = payload.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or user_id <= 0:
        return False

    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 3. Check that user exists in the database
    if user_id not in database:
        return False

    # 4. Update the email address
    try:
        database[user_id]["email"] = new_email.strip()
    except Exception:
        # In a real application, log the exception
        return False

    return True