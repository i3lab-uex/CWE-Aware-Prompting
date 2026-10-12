import re
from typing import Dict, Any

# Mock database and CSRF token for demonstration purposes
database: Dict[int, Dict[str, Any]] = {
    1: {"email": "old@example.com", "name": "Alice"},
    2: {"email": "bob@example.com", "name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Simple regex for basic email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")


def edit_user_email(req_payload: Dict[str, Any]) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_payload : dict
        HTTP request payload containing headers and body. Expected keys:
            - "headers": dict, must include a 'X-CSRF-Token' entry.
            - "body": dict, must contain:
                * "user_id" : int
                * "new_email" : str

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate request body
    body = req_payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Update the mock database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Optional: Ensure new email is not already used by another user
    for uid, record in database.items():
        if uid != user_id and record.get("email") == new_email:
            return False

    # Perform the update
    user_record["email"] = new_email
    return True