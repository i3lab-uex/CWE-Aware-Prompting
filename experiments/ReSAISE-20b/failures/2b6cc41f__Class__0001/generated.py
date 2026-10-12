import re

# Mock database: user_id -> dict with 'email' field
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"}
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Simple email regex pattern (RFC 5322 compliant is complex; this suffices for demo)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$)"
)

def modify_user_email(req_data: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_data : dict
        Dictionary containing request headers and body.
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

    # 1. CSRF token validation
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user data
    body = req_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or user_id <= 0:
        return False
    if not isinstance(new_email, str) or not new_email.strip():
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Verify user exists in database
    if user_id not in database:
        return False

    # 5. Update email atomically (simple assignment for mock DB)
    database[user_id]["email"] = new_email.strip()
    return True