import re

# Simulated database: {user_id: {"email": "..."}}
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Expected CSRF token for the request
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Simple email validation regex (RFC 5322 simplified)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,}$)"
)

def update_user_email(request: dict) -> bool:
    """
    Update the email address of a user in the simulated database.

    Parameters
    ----------
    request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body": {"user_id": <int>, "new_email": "<string>"}
            }

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate payload
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check user existence
    if user_id not in database:
        return False

    # 5. Update email atomically
    try:
        database[user_id]["email"] = new_email
    except Exception:
        return False

    return True