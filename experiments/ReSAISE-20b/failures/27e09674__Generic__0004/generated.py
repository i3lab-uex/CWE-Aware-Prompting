import re
from typing import Dict

# Simulated in‑memory database: {user_id: {"email": str, ...}}
database: Dict[str, dict] = {}

# Pre‑defined CSRF token
EXPECTED_CSRF_TOKEN: str = "secure_token_12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def change_user_email(query: Dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and input validity.

    Parameters
    ----------
    query : dict
        Dictionary containing request data. Expected keys:
            - 'headers': dict, must include 'X-CSRF-Token'
            - 'body': dict, must contain:
                * 'user_id' : str
                * 'new_email': str

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # Extract headers and body
    headers = query.get("headers", {})
    body = query.get("body", {})

    # 1. CSRF protection
    token = headers.get("X-CSRF-Token")
    if not token or token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Validate presence of user_id and new_email
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not new_email:
        return False

    # 3. Basic email format validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Ensure the user exists in the database
    if user_id not in database:
        return False

    # 5. Update the email
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error results in a failure return
        return False

    return True