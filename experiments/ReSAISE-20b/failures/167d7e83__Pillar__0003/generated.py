import re

# Simulated database: user_id -> {'email': str, ...}
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Expected CSRF token
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def update_user_email(request: dict) -> bool:
    """
    Update the email address of a user.

    Parameters
    ----------
    request : dict
        Should contain:
            - 'headers': dict, must include 'X-CSRF-Token'
            - 'body': dict, must contain 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF protection
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract body data
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic validation of input types
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Email format validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check that the user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update the email address
    try:
        user_record["email"] = new_email
    except Exception:
        # Any unexpected error during the update results in failure
        return False

    return True