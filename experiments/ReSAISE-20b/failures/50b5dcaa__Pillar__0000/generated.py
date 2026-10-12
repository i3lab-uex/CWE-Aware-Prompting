import re
from typing import Dict

# Mock database: user_id -> user record dict
database: Dict[str, Dict] = {
    "1": {"email": "alice@example.com"},
    "2": {"email": "bob@example.org"},
}

# Expected CSRF token for the request
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Simple RFC 5322 compliant regex for email validation
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
    r"@([A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,6}$)"
)


def edit_user_email(req_payload: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input.

    Parameters
    ----------
    req_payload : dict
        HTTP request payload containing:
            - headers: dict, may include 'X-CSRF-Token'
            - body: dict with keys:
                * 'user_id': str
                * 'new_email': str

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract user ID and new email from body
    body = req_payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not new_email:
        # Missing required fields
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that the user exists
    if user_id not in database:
        return False

    # 5. Update the email
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # Any unforeseen error during update
        return False