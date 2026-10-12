import re
from typing import Dict

# Mock database: key = user_id, value = dict with user attributes
database: Dict[str, Dict] = {
    "1": {"email": "alice@example.com", "name": "Alice"},
    "2": {"email": "bob@example.com",   "name": "Bob"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token-123"

# Simple email regex (not exhaustive but sufficient for demo)
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def modify_user_email(req_data: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Parameters
    ----------
    req_data : dict
        HTTP request representation containing:
          - headers: dict with a 'X-CSRF-Token' key
          - body   : dict containing 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. CSRF protection
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token
        return False

    # 2. Extract required fields from body
    body = req_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not new_email:
        # Missing required data
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Update the database atomically
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    try:
        # In a real scenario, this would be an atomic DB transaction
        user_record["email"] = new_email
    except Exception:
        # Any unexpected error during update
        return False

    return True