import re
from typing import Dict

# Simulated database and CSRF token for the example
database: Dict[int, dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def _is_valid_email(email: str) -> bool:
    """Return True if the email address matches a simple pattern."""
    return bool(EMAIL_REGEX.match(email))


def modify_user_email_address(user_request: Dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and input validity.

    Parameters
    ----------
    user_request : dict
        Expected to contain:
            - headers: dict with a 'X-CSRF-Token' key
            - body: dict with keys 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated, False otherwise.
    """
    # 1. CSRF token verification
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Retrieve body parameters
    body = user_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Validate new email address
    if not _is_valid_email(new_email):
        return False

    # 4. Check that the user exists in the database
    if user_id not in database:
        return False

    # 5. Update the email address
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # In a real application, log the exception.
        return False