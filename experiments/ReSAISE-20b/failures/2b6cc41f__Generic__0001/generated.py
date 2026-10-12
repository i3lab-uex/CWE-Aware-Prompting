import re
from typing import Dict

# Mock database: user_id -> dict with 'email' field
database: Dict[int, Dict[str, str]] = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@example.com"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN: str = "s3cr3t-t0k3n"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def modify_user_email(req_data: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_data : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': mapping of header names to values
            - 'body':   mapping with user data, e.g.
                        {'user_id': 1, 'new_email': 'foo@bar.com'}

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user data
    body = req_data.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"].strip()
    except (KeyError, ValueError, AttributeError):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Perform the update
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Prevent trivial assignment of same email
    if user_record.get("email") == new_email:
        return True

    # Update the email
    user_record["email"] = new_email
    return True