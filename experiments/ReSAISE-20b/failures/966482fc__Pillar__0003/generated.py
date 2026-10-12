import re

# Mock database and CSRF token for the example
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"}
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")


def modify_user_email(req: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req : dict
        Request payload expected to contain:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict with keys 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. CSRF protection
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or invalid
        return False

    # 2. Extract user ID and new email from body
    body = req.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"].strip()
    except (KeyError, ValueError):
        # Missing or malformed data
        return False

    # 3. Validate new email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Verify user exists in the database
    if user_id not in database:
        return False

    # 5. Update the email
    database[user_id]["email"] = new_email
    return True