import re
from typing import Dict

# Mock database and CSRF token (normally these would be provided by the framework)
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_token_123"

# Simple regex for basic email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")


def edit_user_email(req_payload: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Parameters
    ----------
    req_payload : dict
        The HTTP request payload. Expected to contain:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    try:
        headers = req_payload["headers"]
        csrf_token = headers.get("X-CSRF-Token")
    except (KeyError, AttributeError):
        # Missing headers or headers not a dict
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract user_id and new_email from body
    try:
        body = req_payload["body"]
        user_id_raw = body.get("user_id")
        new_email = body.get("new_email")
    except (KeyError, AttributeError):
        return False

    # Validate that user_id is an integer and exists in the database
    if not isinstance(user_id_raw, int):
        return False

    user = database.get(user_id_raw)
    if not user:
        # User does not exist
        return False

    # 3. Validate new_email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 4. Perform the update
    try:
        user["email"] = new_email
        return True
    except Exception:
        # Catch unexpected errors during update (e.g., immutable mapping)
        return False