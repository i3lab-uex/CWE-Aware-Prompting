import re
from typing import Dict

# Constants (would normally be defined elsewhere)
EXPECTED_CSRF_TOKEN = "S3cUrE_T0kEn_12345"

# Mock database: mapping user_id -> dict with at least an 'email' field
database: Dict[str, Dict[str, str]] = {
    "user1": {"email": "alice@example.com"},
    "user2": {"email": "bob@example.org"},
}

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
)

def modify_user_email(req: Dict) -> bool:
    """
    Update a user's email address in the mock database after performing
    CSRF protection and basic validation.

    Parameters:
        req (dict): A dictionary that must contain a 'headers' key with
                    a 'X-CSRF-Token' header and a 'body' key with JSON-like
                    data including 'user_id' and 'new_email'.

    Returns:
        bool: True if the update succeeded, False otherwise.
    """
    # 1. CSRF token validation
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF check failed
        return False

    # 2. Extract user ID and new email from the request body
    body = req.get("body", {})
    user_id = str(body.get("user_id")).strip()
    new_email = body.get("new_email", "").strip()

    if not user_id or not new_email:
        # Missing required fields
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Verify that the user exists in the database
    if user_id not in database:
        return False

    # 5. Update the email address
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # In a real application you might log the exception
        return False

    return True