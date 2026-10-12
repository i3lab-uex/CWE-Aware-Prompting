import re
import hmac
from typing import Dict, Any

# Constants and mock database (would normally be imported or passed in)
EXPECTED_CSRF_TOKEN: str = "s3cureT0ken123"
database: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Simple regex for email validation (not exhaustive but sufficient for demo)
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z0-9]{2,}$")


def _is_valid_email(email: str) -> bool:
    """Return True if email matches the simple regex."""
    return EMAIL_REGEX.match(email) is not None


def change_user_email(query: Dict[str, Any]) -> bool:
    """
    Update a user's email address after verifying CSRF token and input data.

    Parameters
    ----------
    query : dict
        Dictionary representing the HTTP request. Expected keys:
            - 'headers': dict containing at least 'X-CSRF-Token'
            - 'body': dict with keys 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.

    Notes
    -----
    - The function uses a constant-time comparison for the CSRF token to mitigate timing attacks.
    - It performs basic validation on the email format and checks that the user exists in the database.
    """
    # 1. Validate request structure
    if not isinstance(query, dict):
        return False

    headers = query.get("headers")
    body = query.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF token verification
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False

    # Constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Extract and validate user_id
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 4. Extract and validate new email
    new_email = body.get("new_email")
    if not isinstance(new_email, str) or not _is_valid_email(new_email):
        return False

    # 5. Update the mock database
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        return False

    # Perform the update
    user_record["email"] = new_email
    return True