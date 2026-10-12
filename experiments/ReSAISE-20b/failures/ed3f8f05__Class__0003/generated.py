import re
from typing import Dict, Any

# Mock database and CSRF token (for illustration only)
database: Dict[int, Dict[str, Any]] = {
    1: {"email": "old@example.com", "name": "Alice"},
    2: {"email": "bob@example.com", "name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a very simple email validation
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")

def change_user_email(request_data: Dict[str, Any]) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request. Expected keys:
            - headers: dict containing at least 'X-CSRF-Token'
            - body: dict containing 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID and new email from the body
    body = request_data.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Basic email format validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Ensure the user exists
    if user_id not in database:
        return False

    # 5. Update the email atomically
    try:
        database[user_id]["email"] = new_email
    except Exception:
        return False

    return True