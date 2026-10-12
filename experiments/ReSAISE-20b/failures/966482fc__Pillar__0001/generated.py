import re

# Simulated database and CSRF token
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.net"}
}
EXPECTED_CSRF_TOKEN = "securetoken123"

# Simple regex for email validation (RFC 5322 simplified)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$)"
)

def modify_user_email(req: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req : dict
        The request dictionary. Expected keys:
            - 'headers': dict containing 'X-CSRF-Token'
            - 'body': dict containing 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. CSRF protection
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or invalid
        return False

    # 2. Extract body data
    body = req.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic validation
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Email format validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check user existence
    if user_id not in database:
        return False

    # 6. Update the email
    try:
        database[user_id]["email"] = new_email.strip()
    except Exception:
        # Unexpected failure during update
        return False

    return True