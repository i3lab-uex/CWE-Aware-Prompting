import re

# Simulated database of users: {user_id: {"email": str}}
database = {}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def change_user_email(new_request: dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    new_request : dict
        Incoming request object containing:
            - headers: dict, should contain 'X-CSRF-Token'
            - body: dict, must include 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = new_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = new_request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic type and presence checks
    if not isinstance(user_id, str) or not user_id:
        return False
    if not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check that the user exists
    if user_id not in database:
        return False

    # 6. Update the email
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # In case the user record is malformed or not a dict
        return False

    return True