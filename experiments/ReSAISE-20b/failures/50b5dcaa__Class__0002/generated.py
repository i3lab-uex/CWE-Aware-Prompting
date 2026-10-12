import re

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Mock database: mapping user_id (int) to a dict containing at least an 'email' field
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

# Regular expression for a very simple email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def edit_user_email(req_payload: dict) -> bool:
    """
    Update a user's email address after verifying CSRF token, user existence,
    and basic email format.

    Parameters
    ----------
    req_payload : dict
        The HTTP request payload. Expected keys:
            - headers: dict containing 'X-CSRF-Token'
            - body: dict containing 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract and validate payload data
    body = req_payload.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"].strip()
    except (KeyError, TypeError, ValueError):
        # Missing or malformed fields
        return False

    # 3. Basic email format validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Ensure the user exists in the mock database
    if user_id not in database:
        return False

    # 5. Perform the update
    database[user_id]["email"] = new_email
    return True