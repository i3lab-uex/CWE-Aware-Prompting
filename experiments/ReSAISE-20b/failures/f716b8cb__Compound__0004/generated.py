import re

# Simulated global resources
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"}
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

def modify_user_email_address(user_request: dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and input validity.

    Parameters
    ----------
    user_request : dict
        Dictionary representing the HTTP request. Expected keys:
            - 'headers': dict, containing at least 'X-CSRF-Token'
            - 'body': dict, containing 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate request body
    body = user_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"]
    except (KeyError, ValueError):
        return False

    # 3. Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 4. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Optional: ensure the new email is different
    if user_record.get("email") == new_email:
        return True  # nothing to change, but considered successful

    user_record["email"] = new_email
    return True