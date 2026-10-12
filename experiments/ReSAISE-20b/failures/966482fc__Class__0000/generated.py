import re
from typing import Dict

# Mock database and CSRF token
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure_token_12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def modify_user_email(req: Dict) -> bool:
    """
    Modify a user's email address in the mock database.

    Parameters
    ----------
    req : dict
        The request containing headers and body data.
        Expected keys:
            - "headers": {"X-CSRF-Token": str}
            - "body": {"user_id": int, "new_email": str}

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # 1. Validate CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate request body
    body = req.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Ensure user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the email
    try:
        user_record["email"] = new_email
        return True
    except Exception:
        # Log exception in real application; here we simply fail safely.
        return False