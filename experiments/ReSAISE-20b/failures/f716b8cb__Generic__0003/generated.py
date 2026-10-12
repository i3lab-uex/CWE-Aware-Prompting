import re

# Simulated database and CSRF token for demonstration purposes
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def _is_valid_email(email: str) -> bool:
    """
    Very basic email validation using a regular expression.
    For production use, consider more robust libraries like `email-validator`.
    """
    email_regex = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    )
    return bool(email_regex.match(email))

def modify_user_email_address(user_request: dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    user_request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id": <int>,
                    "new_email": "<email>"
                }
            }

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID and new email from body
    body = user_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Validate email format
    if not _is_valid_email(new_email):
        return False

    # 4. Check user exists in database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update email
    try:
        database[user_id]["email"] = new_email
    except Exception:
        return False

    return True