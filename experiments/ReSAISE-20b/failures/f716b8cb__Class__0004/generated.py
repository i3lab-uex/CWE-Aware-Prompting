import re
from typing import Dict

# Simulated global context (would normally be passed or accessed via a framework)
database: Dict[str, dict] = {
    "1": {"email": "old@example.com", "name": "Alice"},
    "2": {"email": "bob@example.org", "name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Simple RFC 5322 compliant email regex (not exhaustive but sufficient for demo)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$)"
)

def modify_user_email_address(user_request: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input.

    Parameters
    ----------
    user_request : dict
        Expected keys:
            - headers: dict, must contain 'X-CSRF-Token'
            - body   : dict, must contain 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if update succeeded, False otherwise.
    """
    # 1. Validate CSRF token (CWE-345: insufficient verification)
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body parameters
    body = user_request.get("body", {})
    user_id = str(body.get("user_id"))  # ensure string key
    new_email = body.get("new_email")

    if not user_id or not new_email:
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Ensure user exists
    if user_id not in database:
        return False

    # 5. Update email
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # Any unexpected failure should not leak details
        return False