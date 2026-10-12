import re

# Mock database and CSRF token for demonstration purposes
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z0-9]{2,}$")


def modify_user_email(req: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req : dict
        Request dictionary expected to contain:
            - 'headers': a mapping of request headers.
            - 'body': a mapping with keys 'user_id' (int) and 'new_email' (str).

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """

    # 1. Verify CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing token
        return False

    # 2. Extract user ID and new email from body
    body = req.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"].strip()
    except (KeyError, ValueError):
        # Missing or invalid data
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that the user exists
    if user_id not in database:
        return False

    # 5. Update the email
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error during the update should result in failure
        return False

    return True