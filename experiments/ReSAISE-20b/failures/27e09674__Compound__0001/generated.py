import re
from typing import Dict

# Simulated database: user_id -> {'email': str, ...}
database: Dict[str, dict] = {
    "user123": {"email": "old@example.com"},
    "user456": {"email": "another@example.com"},
}

# Expected CSRF token
EXPECTED_CSRF_TOKEN = "secure_token_12345"

# Simple email validation regex (RFC 5322 is complex; this covers common cases)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$)"
)


def change_user_email(query: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    query : dict
        The request payload containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict, must contain 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = query.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID and new email
    body = query.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not new_email:
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update email
    try:
        user_record["email"] = new_email
        return True
    except Exception:
        # In a real scenario, log the exception
        return False


# Example usage (for testing purposes)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "new_email": "new@example.com"},
    }
    result = change_user_email(request)
    print("Update successful:", result)
    print("Updated database entry:", database["user123"])