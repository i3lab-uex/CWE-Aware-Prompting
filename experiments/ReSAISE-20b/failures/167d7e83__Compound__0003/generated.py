import re

# Simulated database (for illustration only)
database = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@domain.com"}
}

# Expected CSRF token (would normally be stored securely)
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Simple email regex (not exhaustive but sufficient for demo)
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
    r"@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}$)"
)


def update_user_email(request: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and email format.

    Args:
        request (dict): Should contain:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' and 'new_email'

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    try:
        # 1. CSRF protection
        headers = request.get("headers", {})
        token = headers.get("X-CSRF-Token")
        if token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract and validate request body
        body = request.get("body", {})
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        if user_id is None or new_email is None:
            return False

        # 3. Validate email format
        if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
            return False

        # 4. Ensure user exists
        if user_id not in database:
            return False

        # 5. Update email
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # Log exception in real application; here we simply fail safely
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": "secure_token_123"},
        "body": {"user_id": 1, "new_email": "new@example.com"}
    }
    print(update_user_email(req))  # Expected: True
    print(database[1]["email"])   # Expected: new@example.com