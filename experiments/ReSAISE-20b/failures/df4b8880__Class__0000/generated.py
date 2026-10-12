import re

# Pre‑defined CSRF token used for validation
EXPECTED_CSRF_TOKEN = "12345-abcde"

# Simple regex for validating email addresses
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}"
    r"[a-zA-Z0-9])?(?:\.[a-zA-Z]{2,})+$)"
)

def alter_user_email(payload: dict, database: dict) -> bool:
    """
    Update a user's email address in the mock `database`.

    Parameters
    ----------
    payload : dict
        Dictionary containing request headers and body. Expected keys:
            - 'headers': mapping of header names to values
            - 'body'   : mapping with keys 'user_id' and 'new_email'
    database : dict
        Dictionary simulating user storage. Keys are user IDs, values are
        dictionaries containing at least an 'email' field.

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch – possible CSRF or tampered request
        return False

    # 2. Extract user ID and new email from body
    body = payload.get("body", {})
    try:
        user_id = str(body["user_id"])
        new_email = body["new_email"]
    except (KeyError, TypeError):
        # Missing required fields
        return False

    # 3. Validate new email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        # Invalid email – reject to prevent injection/invalid data
        return False

    # 4. Check that the user exists in the database
    if user_id not in database:
        return False

    # 5. Update the user's email
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error (e.g., immutable dict) should be treated as failure
        return False

    return True