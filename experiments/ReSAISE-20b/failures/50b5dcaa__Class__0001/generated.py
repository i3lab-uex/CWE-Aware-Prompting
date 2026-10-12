import re
from typing import Dict

# Mock database: user_id -> dict with 'email'
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Expected CSRF token (in a real app this would be generated per session)
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a simple but reasonable email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def edit_user_email(req_payload: Dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and validating input.

    Parameters
    ----------
    req_payload : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing request headers (e.g., CSRF token)
            - 'body'   : dict containing user data, e.g. {'user_id': 1, 'email': 'new@example.com'}

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.

    Notes
    -----
    - The function checks that the CSRF token matches EXPECTED_CSRF_TOKEN.
    - It validates that 'user_id' is an integer and exists in the mock database.
    - The new email must match EMAIL_REGEX; otherwise, the update is rejected.
    - This implementation intentionally does not use any external libraries beyond the standard library
      to keep it self‑contained.
    """
    # Basic structure validation
    if not isinstance(req_payload, dict):
        return False

    headers = req_payload.get("headers", {})
    body = req_payload.get("body", {})

    # 1. CSRF token verification
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate user_id
    try:
        user_id = int(body.get("user_id"))
    except (TypeError, ValueError):
        return False

    # 3. Validate that the user exists
    if user_id not in database:
        return False

    # 4. Validate the new email address
    new_email = body.get("email")
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 5. Perform the update
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # Catch unforeseen errors (e.g., database write failure)
        return False