import re
from typing import Dict

# Simulated database and CSRF token (these would normally be provided by the surrounding context)
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
)

def edit_user_email(payload: Dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    payload : dict
        The incoming request object. It must contain:
            - headers: a mapping that includes the 'X-CSRF-Token' key.
            - body: a mapping that contains:
                * user_id : int
                * new_email : str

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Notes
    -----
    The function performs several security checks to mitigate CWE-345:
        * CSRF token validation
        * User existence check
        * Email format validation
    """
    # 1. Validate presence of headers and CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body parameters
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate types
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Verify user exists in database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error results in failure
        return False

    return True