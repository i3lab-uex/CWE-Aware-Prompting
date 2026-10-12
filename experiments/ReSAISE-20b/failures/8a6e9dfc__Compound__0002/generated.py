import re

# Simulated database and expected CSRF token
database = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@domain.org"}
}
EXPECTED_CSRF_TOKEN = "securetoken123"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def edit_user_email(payload: dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and input validity.

    Parameters
    ----------
    payload : dict
        The incoming request object containing headers and body. Expected keys:
            - 'headers': dict, must contain 'X-CSRF-Token'
            - 'body'   : dict, must contain 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Validate body contents
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Perform the update
    user_record["email"] = new_email
    return True