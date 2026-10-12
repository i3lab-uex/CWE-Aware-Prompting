import re
from typing import Dict

# Simulated global database and expected CSRF token
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_token_123"

# Email validation regex (simple RFC 5322 compliant subset)
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+"
    r"(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
    r"@([A-Za-z0-9]([-A-Za-z0-9]*[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,}$)"
)

def change_user_email(new_request: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Args:
        new_request (dict): Incoming request containing headers and body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "..."},
                    "body":   {"user_id": 123, "new_email": "example@example.com"}
                }

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token presence and correctness
    headers = new_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body parameters
    body = new_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"]
    except (KeyError, TypeError, ValueError):
        return False

    # 3. Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that the user exists in the database
    if user_id not in database:
        return False

    # 5. Perform the update
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # Log exception in real application; here we just fail silently
        return False