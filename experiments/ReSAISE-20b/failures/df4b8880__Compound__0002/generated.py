import re
from typing import Dict

# Constants used by the application
EXPECTED_CSRF_TOKEN = "my-secure-csrf-token"

# Simple in‑memory mock database
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def _is_valid_email(email: str) -> bool:
    """Return True if email matches the basic regex pattern."""
    return bool(EMAIL_REGEX.match(email))

def alter_user_email(payload: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    payload : dict
        The request payload containing:
            - headers: dict (must contain 'X-CSRF-Token')
            - body: dict (must contain 'user_id' and 'new_email')

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. CSRF token validation
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = payload.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"]
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Validate email format
    if not _is_valid_email(new_email):
        return False

    # 4. Check user existence
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update email
    user_record["email"] = new_email
    return True

# Example usage (for demonstration purposes only)
if __name__ == "__main__":
    test_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(alter_user_email(test_payload))  # Expected: True
    print(database[1]["email"])            # Expected: alice.new@example.com