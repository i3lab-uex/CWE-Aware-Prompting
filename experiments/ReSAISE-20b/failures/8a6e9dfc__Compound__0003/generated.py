import re

# Simulated database (user_id -> user data)
database = {
    1: {"email": "alice@example.com", "name": "Alice"},
    2: {"email": "bob@example.com", "name": "Bob"},
}

# Expected CSRF token (in a real app this would be stored per session)
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Simple email validation regex
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z0-9]{2,}$")


def edit_user_email(payload: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Parameters
    ----------
    payload : dict
        Incoming request containing 'headers' and 'body'.
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {"user_id": <int>, "new_email": "<string>"}
            }

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token
        return False

    # 2. Validate body structure and content
    body = payload.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or user_id <= 0:
        return False
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 3. Check if user exists
    user = database.get(user_id)
    if not user:
        return False

    # 4. Update email
    try:
        database[user_id]["email"] = new_email.strip()
        return True
    except Exception:
        # Log exception in real application; here we simply fail safely.
        return False