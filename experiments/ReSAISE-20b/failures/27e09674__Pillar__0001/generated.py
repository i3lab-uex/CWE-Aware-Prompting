import re
from typing import Dict

# Predefined CSRF token for the application
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token"

# Mock database: mapping user ID to a dictionary of user data
database: Dict[str, Dict] = {
    "1": {"email": "alice@example.com"},
    "2": {"email": "bob@example.com"},
}


def is_valid_email(email: str) -> bool:
    """
    Very simple email validation using a regex.
    For production use, consider more robust validation or dedicated libraries.
    """
    pattern = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    )
    return bool(pattern.match(email))


def change_user_email(query: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token,
    presence of required fields, and email format.

    Parameters
    ----------
    query : dict
        The request dictionary containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict, must include 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = query.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = query.get("body", {})
    user_id = str(body.get("user_id"))  # ensure string key
    new_email = body.get("new_email")

    if not user_id or not new_email:
        return False

    # 3. Validate email format
    if not is_valid_email(new_email):
        return False

    # 4. Check user exists in database
    if user_id not in database:
        return False

    # 5. Update email
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # In a real system, log the exception here.
        return False

    return True