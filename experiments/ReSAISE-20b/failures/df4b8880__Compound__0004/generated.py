import re
from typing import Dict, Any

# Expected CSRF token (would normally be stored securely)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Mock database: user_id -> { 'email': str, ... }
database: Dict[str, Dict[str, Any]] = {
    "1": {"email": "alice@example.com"},
    "2": {"email": "bob@example.org"},
}

# Simple email regex (not fully RFC compliant but sufficient for demo)
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def alter_user_email(payload: Dict[str, Any]) -> bool:
    """
    Update a user's email address after verifying CSRF token and input validity.

    Parameters
    ----------
    payload : dict
        Request data containing:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' and 'email'

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Verify CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract user_id and new email from body
    body = payload.get("body", {})
    user_id = str(body.get("user_id"))
    new_email = body.get("email", "").strip()

    if not user_id or not new_email:
        # Missing required fields
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that the user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the email
    try:
        user_record["email"] = new_email
    except Exception:
        # In case the database structure is unexpected or write fails
        return False

    return True


# Example usage:
if __name__ == "__main__":
    test_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "1", "email": "newalice@example.com"},
    }
    success = alter_user_email(test_payload)
    print("Update succeeded:", success)
    print("Updated database entry:", database["1"])