import json
import re

# Simulated global data
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"}
}
EXPECTED_CSRF_TOKEN = "secret_csrf_token_123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def modify_user_email_address(user_request: dict) -> bool:
    """
    Update a user's email address after validating CSRF token, user ID,
    and new email format.

    Args:
        user_request (dict): Incoming request with 'headers' and 'body'.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body": '{"user_id": 1, "new_email": "alice@new.com"}'
                }

    Returns:
        bool: True if the email was updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Parse JSON body
    try:
        body = json.loads(user_request.get("body", "{}"))
    except (json.JSONDecodeError, TypeError):
        return False

    # 3. Extract user ID and new email
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Verify user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update email
    user_record["email"] = new_email
    return True