import re
from typing import Dict

# Simulated database and CSRF token (would normally be imported or passed in)
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
    r"@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}$)"
)

def modify_user_email_address(user_request: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and email format.

    Parameters
    ----------
    user_request : dict
        Incoming request containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict with keys:
                - 'user_id': int
                - 'new_email': str

    Returns
    -------
    bool
        True if update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body fields
    body = user_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that user exists in the database
    if user_id not in database:
        return False

    # 5. Update the email address
    try:
        database[user_id]["email"] = new_email
    except Exception:
        return False

    return True