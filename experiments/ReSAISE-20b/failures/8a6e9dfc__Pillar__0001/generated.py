import re

# Simulated database and CSRF token for the application
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def edit_user_email(payload: dict) -> bool:
    """
    Update a user's email address after validating the CSRF token and
    ensuring that the user exists and the new email is valid.

    Parameters
    ----------
    payload : dict
        Incoming request containing headers and body. Expected structure:
        {
            "headers": {"X-CSRF-Token": "<token>"},
            "body":   {
                "user_id": int,
                "new_email": str
            }
        }

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    try:
        headers = payload["headers"]
        csrf_token = headers.get("X-CSRF-Token")
    except (KeyError, TypeError):
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID and new email
    try:
        body = payload["body"]
        user_id = int(body["user_id"])
        new_email = body["new_email"].strip()
    except (KeyError, TypeError, ValueError):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that the user exists
    if user_id not in database:
        return False

    # 5. Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error during the update should not expose internal state
        return False

    return True