import re
from typing import Dict

# Constants used for CSRF protection and email validation
EXPECTED_CSRF_TOKEN = "s3cure-t0k3n-12345"
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")

def change_user_email(query: Dict) -> bool:
    """
    Update a user's email address in the mock database after performing
    CSRF protection and basic validation.

    Parameters
    ----------
    query : dict
        The incoming request data containing:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' (int or str) and 'new_email' (str)

    Returns
    -------
    bool
        True if the update succeeds, False otherwise.
    """
    # 1. CSRF protection
    headers = query.get("headers", {})
    token = headers.get("X-CSRF-Token")
    if token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token – reject the request
        return False

    # 2. Extract payload and validate presence of required fields
    body = query.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if user_id is None or new_email is None:
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Update the mock database
    if user_id in database:
        database[user_id]["email"] = new_email
        return True

    # User not found – fail gracefully
    return False


# Mock database for demonstration purposes
database: Dict = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"}
}