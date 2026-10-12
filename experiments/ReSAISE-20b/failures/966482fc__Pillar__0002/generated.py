import re
import hmac
from typing import Dict

# Mock database: user_id -> user data dictionary
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Predefined CSRF token used for protection
EXPECTED_CSRF_TOKEN: str = "s3cr3t-csrf-token"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def modify_user_email(req: Dict) -> bool:
    """
    Update a user's email address in the mock database after validating
    CSRF token, user ID, and new email format.

    Parameters
    ----------
    req : dict
        Expected keys:
            - 'headers': dict containing HTTP headers (e.g., 'X-CSRF-Token')
            - 'body'   : dict containing:
                * 'user_id': int
                * 'new_email': str

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract body data
    body = req.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"].strip()
    except (KeyError, ValueError):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Verify user exists
    user = database.get(user_id)
    if not user:
        return False

    # 5. Update email
    user["email"] = new_email
    return True