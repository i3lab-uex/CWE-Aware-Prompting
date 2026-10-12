import re
from typing import Dict

# Simulated database and CSRF token (for demonstration purposes)
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_token_123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")


def edit_user_email(payload: Dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Args:
        payload (dict): Incoming request containing 'headers' and 'body'.
            - headers: dict with key 'X-CSRF-Token'
            - body: dict with keys 'user_id' (int) and 'new_email' (str)

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID and new email
    body = payload.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"]
    except (KeyError, ValueError):
        return False

    # 3. Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 4. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Prevent accidental type coercion: ensure only email is updated
    user_record["email"] = new_email
    return True