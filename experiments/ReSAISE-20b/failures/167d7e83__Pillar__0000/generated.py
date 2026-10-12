import re

# Simulated database: user_id -> { "email": str, ... }
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"}
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Simple email regex (RFC 5322 compliant part)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}"
    r"[a-zA-Z0-9])?(?:\.[a-zA-Z0-9]"
    r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$)"
)

def _is_valid_email(email: str) -> bool:
    """Return True if email matches a simple RFC 5322 regex."""
    return EMAIL_REGEX.fullmatch(email) is not None

def update_user_email(request: dict) -> bool:
    """
    Update the email address of a user.

    Args:
        request (dict): Should contain:
            - 'headers': dict with key 'X-CSRF-Token'
            - 'body': dict with keys:
                * 'user_id' (int)
                * 'new_email' (str)

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    # 1. CSRF protection
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False  # CSRF validation failed

    # 2. Validate request body
    body = request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"]
    except (KeyError, ValueError, TypeError):
        return False  # Missing or invalid data

    # 3. Validate email format
    if not _is_valid_email(new_email):
        return False

    # 4. Check user existence
    user = database.get(user_id)
    if not user:
        return False

    # 5. Update email
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # In a real system, log the exception securely
        return False

# Example usage (for testing purposes)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"}
    }
    print(update_user_email(req))  # Should output: True
    print(database[1]["email"])   # Should show the updated email