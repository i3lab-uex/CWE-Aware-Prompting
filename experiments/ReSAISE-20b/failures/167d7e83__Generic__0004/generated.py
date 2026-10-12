import re
from typing import Dict, Any

# Expected CSRF token for the request (would normally be stored securely)
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_value"

# Simple email validation regex (RFC 5322 compliant is complex; this covers most common cases)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+"
    r"(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,}$)"
)

def update_user_email(request: Dict[str, Any], database: Dict[int, Dict[str, Any]]) -> bool:
    """
    Update a user's email address.

    Parameters
    ----------
    request : dict
        Dictionary containing request data. Expected keys:
            - 'headers': dict with at least 'X-CSRF-Token'
            - 'body': dict with keys 'user_id' (int) and 'new_email' (str)
    database : dict
        Simulated user database mapping user IDs to user info dicts.

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF protection
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate input
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Email format validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check user existence
    user = database.get(user_id)
    if not user:
        return False

    # 5. Update the email
    try:
        user["email"] = new_email.strip()
    except Exception:
        return False

    # 6. Success
    return True