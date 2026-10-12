import re
import hmac
from typing import Dict

# Mock database: {user_id: {"email": str}}
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}

# Expected CSRF token (in a real app this would be generated per session)
EXPECTED_CSRF_TOKEN = "s3cure-t0k3n"

# Regular expression for a very simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def _is_csrf_token_valid(token: str) -> bool:
    """
    Validate the CSRF token using a constant‑time comparison to avoid timing attacks.
    """
    return hmac.compare_digest(token, EXPECTED_CSRF_TOKEN)


def change_user_email(request_data: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    request_data : dict
        Expected keys:
            - "headers": dict, must contain "X-CSRF-Token"
            - "body": dict, must contain "user_id" (int) and "new_email" (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    try:
        headers = request_data.get("headers", {})
        body = request_data.get("body", {})

        # 1. CSRF protection
        csrf_token = headers.get("X-CSRF-Token", "")
        if not _is_csrf_token_valid(csrf_token):
            return False

        # 2. Retrieve user ID and new email
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        if not isinstance(user_id, int) or not isinstance(new_email, str):
            return False

        # 3. Validate email format
        if not EMAIL_REGEX.match(new_email):
            return False

        # 4. Ensure the new email is not already used by another user
        for uid, data in database.items():
            if uid != user_id and data.get("email") == new_email:
                return False

        # 5. Update the database
        if user_id in database:
            database[user_id]["email"] = new_email
            return True

        # User not found
        return False

    except Exception:
        # Log exception in real application; here we simply fail safely
        return False