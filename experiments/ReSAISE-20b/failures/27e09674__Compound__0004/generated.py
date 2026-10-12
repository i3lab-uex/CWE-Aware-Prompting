import re
from typing import Dict

# Simulated database of users: {user_id: {"email": str}}
database: Dict[int, dict] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Predefined CSRF token used by the application
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}$"
)

def change_user_email(query: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    query : dict
        The request payload, expected to contain:
            - 'headers': a dict with the key 'X-CSRF-Token'
            - 'body':   a dict with keys 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # 1. Validate CSRF token
    headers = query.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract body data
    body = query.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic type and presence checks
    if not isinstance(user_id, int):
        return False
    if not isinstance(new_email, str) or not new_email:
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check that user exists in the database
    if user_id not in database:
        return False

    # 6. Update the email
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Unexpected error during update
        return False

    return True