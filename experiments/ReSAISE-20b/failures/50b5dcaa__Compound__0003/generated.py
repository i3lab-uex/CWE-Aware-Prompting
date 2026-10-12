import re

# Constants and mock database (for demonstration purposes)
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token"
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

def _is_valid_email(email: str) -> bool:
    """
    Basic email validation using a regex.
    This is not exhaustive but catches most common cases.
    """
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None

def edit_user_email(req_payload: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_payload : dict
        The HTTP request payload. Expected structure:
        {
            "headers": {"X-CSRF-Token": "<token>"},
            "body": {"user_id": <int>, "new_email": "<email>"}
        }

    Returns
    -------
    bool
        True if the email was successfully updated; False otherwise.
    """
    # 1. CSRF protection
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract user ID and new email from the request body
    body = req_payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # Basic type checks
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not _is_valid_email(new_email):
        return False

    # 4. Check that the user exists in the database
    if user_id not in database:
        return False

    # 5. Update the email address
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Catch any unexpected errors during update
        return False

    return True