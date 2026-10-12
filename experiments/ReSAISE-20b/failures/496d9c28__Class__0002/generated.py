import re

# Simulated database and CSRF token for demonstration purposes.
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for basic email validation.
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$")


def change_user_email(new_request: dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    new_request : dict
        The incoming request object. Expected to contain:
            - headers: a dict that may include 'X-CSRF-Token'
            - body: a dict with keys:
                * user_id (int)
                * new_email (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Notes
    -----
    - Validates CSRF token to mitigate replay attacks (CWE-345).
    - Checks that the user exists in the database.
    - Validates the format of the new email address.
    """
    # 1. Verify CSRF token
    headers = new_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = new_request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic type checks
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Verify user exists
    if user_id not in database:
        return False

    # 6. Update email atomically
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unforeseen error should not expose internal state.
        return False

    return True