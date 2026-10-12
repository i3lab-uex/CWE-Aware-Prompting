import re

# Mock database and CSRF token for demonstration purposes
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)

def is_valid_email(email: str) -> bool:
    """
    Basic email validation using a regex.
    This is intentionally simple to avoid excessive complexity
    while still preventing obvious malformed addresses.
    """
    return bool(EMAIL_REGEX.match(email))

def modify_user_email(req: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req : dict
        Request data containing:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    try:
        # 1. CSRF token verification
        headers = req.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract user ID and new email
        body = req.get("body", {})
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        # 3. Basic type checks
        if not isinstance(user_id, int) or not isinstance(new_email, str):
            return False

        # 4. Validate email format
        if not is_valid_email(new_email):
            return False

        # 5. Verify user exists in database
        if user_id not in database:
            return False

        # 6. Update the email
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # Any unexpected error results in a failure
        return False