import re
from typing import Dict

# Simulated database: {user_id: {"email": str, ...}}
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Expected CSRF token (would normally be stored per session)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def change_user_email(new_request: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input.

    Parameters
    ----------
    new_request : dict
        Incoming request object containing:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with keys 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = new_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract and validate body data
    body = new_request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # Ensure user_id is an integer and exists in the database
    if not isinstance(user_id, int) or user_id not in database:
        return False

    # Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 3. Perform the update
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # Any unexpected error should result in a failure response
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": "secure_csrf_token_123"},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(change_user_email(request))  # Expected: True
    print(database[1]["email"])        # Expected: 'alice.new@example.com'