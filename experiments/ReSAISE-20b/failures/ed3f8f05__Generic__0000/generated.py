import re

# Mock database: user_id -> dict with 'email' field
database = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@domain.org"},
}

# Expected CSRF token for the session
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Regular expression for a very simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)

def change_user_email(request_data: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request. Must contain:
            - 'headers': dict, should include 'X-CSRF-Token'
            - 'body'   : dict, must contain 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract user_id and new_email from body
    body = request_data.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError, TypeError):
        # Missing or malformed data
        return False

    # 3. Basic email validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Update the mock database
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Perform the update (in a real scenario, you would also handle persistence)
    user_record["email"] = new_email
    return True