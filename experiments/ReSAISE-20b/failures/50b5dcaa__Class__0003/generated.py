import re

# Mock database and CSRF token for demonstration purposes
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"}
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")


def edit_user_email(req_payload: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_payload : dict
        Dictionary containing request data. Expected keys:
            - headers: dict with at least 'X-CSRF-Token'
            - body: dict containing:
                * user_id (int)
                * new_email (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """

    # 1. Validate CSRF token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user_id and new_email
    body = req_payload.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Verify that the user exists
    if user_id not in database:
        return False

    # 4. Validate the new email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Update the email
    database[user_id]["email"] = new_email
    return True