import re
from typing import Dict

# Simulated environment constants
EXPECTED_CSRF_TOKEN = "secure_token_12345"
database: Dict[int, Dict[str, str]] = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@example.org"},
}

# Simple email regex for basic validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def change_user_email(query: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    query : dict
        Expected to contain:
            - headers: dict with 'X-CSRF-Token' key
            - body: dict with 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.

    Notes
    -----
    * Validates CSRF token to mitigate cross‑site request forgery.
    * Performs basic type and format checks on the user ID and email.
    * Returns False if any validation fails or the user does not exist.
    """
    # 1. Basic structure check
    if not isinstance(query, dict):
        return False

    headers = query.get("headers")
    body = query.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF token verification
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 4. Validate new email format
    new_email = body.get("new_email")
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check if user exists
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # 6. Perform the update
    try:
        user_record["email"] = new_email
    except Exception:  # Catch unexpected assignment errors
        return False

    return True