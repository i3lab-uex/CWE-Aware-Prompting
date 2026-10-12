import re
from typing import Dict

# Simulated database and CSRF token (normally these would be stored securely elsewhere)
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "s3cr3t-csrf-token"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)

def modify_user_email(req: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req : dict
        Expected to contain:
            - 'headers': a mapping of request headers.
              Must include 'X-CSRF-Token' with the correct token.
            - 'body': a mapping containing:
                - 'user_id' (int)
                - 'new_email' (str)

    Returns
    -------
    bool
        True if the email was successfully updated; False otherwise.
    """
    # 1. CSRF protection
    headers = req.get("headers", {})
    token = headers.get("X-CSRF-Token")
    if not token or token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract and validate body data
    body = req.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError, TypeError):
        # Missing or malformed data
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check user existence
    if user_id not in database:
        return False

    # 5. Update the email
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # Unexpected error during update (e.g., immutable mapping)
        return False