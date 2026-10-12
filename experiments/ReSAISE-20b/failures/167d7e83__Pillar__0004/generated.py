import re

# Simulated database: user_id -> { "email": ... }
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Expected CSRF token (would normally be stored per session)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Simple email regex for validation (RFC 5322 compliant patterns are complex;
# this pattern covers most common cases).
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$)"
)

def update_user_email(request: dict) -> bool:
    """
    Update a user's email address.

    Parameters
    ----------
    request : dict
        Expected keys:
            - headers: dict, must contain 'X-CSRF-Token'
            - body: dict, must contain 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF protection
    headers = request.get("headers", {})
    token = headers.get("X-CSRF-Token")
    if not token or token != EXPECTED_CSRF_TOKEN:
        # CSRF check failed
        return False

    # 2. Extract and validate input
    body = request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError, TypeError):
        # Missing or invalid parameters
        return False

    if not EMAIL_REGEX.match(new_email):
        # Email format is invalid
        return False

    # 3. Check that user exists
    if user_id not in database:
        return False

    # 4. Perform the update (no SQL injection risk here because we use a dict)
    database[user_id]["email"] = new_email

    return True