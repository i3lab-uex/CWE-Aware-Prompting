import re

# Constants for CSRF protection
EXPECTED_CSRF_TOKEN = "super_secret_token"

# Regular expression for a simple email validation (RFC 5322 compliant regex is complex; this suffices for demo)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def alter_user_email(payload: dict, database: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    payload : dict
        The request containing:
            - headers: a dict with the 'X-CSRF-Token' header.
            - body: a dict with keys 'user_id' and 'new_email'.
    database : dict
        Simulated user storage. Keys are user IDs; values are dicts with an 'email' field.

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. CSRF protection: verify token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or incorrect
        return False

    # 2. Extract user ID and new email from body
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate input
    if not isinstance(user_id, str) or not user_id:
        return False

    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that user exists
    if user_id not in database:
        return False

    # 5. Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error during update
        return False

    return True