import re

# Mock database: user_id -> { "email": str, ... }
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Expected CSRF token for the session
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Simple email regex pattern (RFC 5322 compliant is complex; this suffices for demo)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def edit_user_email(req_payload: dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and validating input.

    Parameters
    ----------
    req_payload : dict
        The HTTP request payload containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict with keys:
                * 'user_id' : int
                * 'new_email': str

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF protection: verify token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user_id and new_email from body
    body = req_payload.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"]
    except (KeyError, TypeError, ValueError):
        return False

    # 3. Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that user exists in the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the email
    user_record["email"] = new_email
    return True

# Example usage:
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice_new@example.com"}
    }
    print(edit_user_email(request))  # Expected: True
    print(database[1]["email"])      # Updated email