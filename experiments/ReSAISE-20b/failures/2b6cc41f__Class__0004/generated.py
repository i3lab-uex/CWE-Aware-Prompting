import re
import hmac
from typing import Dict

# Mock database: user_id -> {'email': str, ...}
database: Dict[str, Dict] = {
    "1": {"email": "alice@example.com"},
    "2": {"email": "bob@example.com"},
}

# CSRF token expected by the server
EXPECTED_CSRF_TOKEN: str = "s3cureT0k3n"

# Regular expression for a simple but reasonably strict email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    """
    return hmac.compare_digest(val1, val2)

def modify_user_email(req_data: Dict) -> bool:
    """
    Update a user's email address.

    Parameters
    ----------
    req_data : dict
        HTTP request data. Expected keys:
            - 'headers': dict containing the CSRF token under 'X-CSRF-Token'
            - 'body': dict containing:
                * 'user_id' : str
                * 'new_email': str

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not _constant_time_compare(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract body data
    body = req_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not new_email:
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Ensure user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update email
    try:
        user_record["email"] = new_email
    except Exception:
        return False

    # 6. Successful update
    return True