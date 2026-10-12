import re
from typing import Dict, Any

# Regular expression for a simple email validation (RFC 5322 compliant regex can be very complex;
# this pattern covers most common cases without being overly permissive)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z]{2,})+$)"
)

def edit_user_email(
    payload: Dict[str, Any],
    database: Dict[int, Dict[str, Any]],
    EXPECTED_CSRF_TOKEN: str
) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    payload : dict
        Incoming request data. Expected keys:
            - 'headers': dict containing at least the key 'X-CSRF-Token'
            - 'body': dict containing 'user_id' (int) and 'new_email' (str)
    database : dict
        Simulated user database. Keys are user IDs and values are user records.
    EXPECTED_CSRF_TOKEN : str
        The correct CSRF token to validate against.

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # Basic payload structure checks
    try:
        headers = payload["headers"]
        body = payload["body"]
        csrf_token = headers.get("X-CSRF-Token", "")
        user_id = body["user_id"]
        new_email = body["new_email"]
    except (KeyError, TypeError):
        # Missing required fields
        return False

    # CSRF token validation
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Email format validation
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # User existence check
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        return False

    # Update email
    user_record["email"] = new_email
    return True