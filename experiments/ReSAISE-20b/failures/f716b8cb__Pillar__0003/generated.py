import re

# Simulated database and expected CSRF token (would normally be secure constants)
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure_token_12345"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def modify_user_email_address(user_request: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and email format.

    Args:
        user_request: Dictionary containing request headers and body.
            Expected keys:
                - "headers": dict with a "X-CSRF-Token" key.
                - "body": dict containing "user_id" (int) and "new_email" (str).

    Returns:
        True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token
        return False

    # 2. Extract body data
    body = user_request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic type checks
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Email format validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check that the user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update the email
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error during update results in failure
        return False

    return True