import re

# Simulated database: user_id -> { "email": str, ... }
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)

def _is_valid_email(email: str) -> bool:
    """Return True if the email matches a basic RFC‑5322 compliant pattern."""
    return bool(EMAIL_REGEX.match(email))

def update_user_email(request: dict) -> bool:
    """
    Update the email address of a user.

    Parameters
    ----------
    request : dict
        Must contain:
            - headers: dict with 'X-CSRF-Token' key.
            - body   : dict with keys 'user_id' (int) and 'new_email' (str).

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. CSRF token validation
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate presence of required fields
    if user_id is None or new_email is None:
        return False

    # 4. Validate email format
    if not _is_valid_email(new_email):
        return False

    # 5. Verify that the user exists
    if user_id not in database:
        return False

    # 6. Perform the update
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # In a real system you would log the exception
        return False

# Example usage (uncomment to test):
# req = {
#     "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
#     "body": {"user_id": 1, "new_email": "alice.new@example.com"}
# }
# print(update_user_email(req))  # Should output: True