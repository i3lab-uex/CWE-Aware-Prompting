import re
from typing import Dict

# Mock database and CSRF token (normally these would be defined elsewhere)
database: Dict[int, dict] = {
    1: {"email": "old@example.com"},
    2: {"email": "user@domain.org"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
    r"@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}$)"
)


def alter_user_email(payload: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and payload data.

    Parameters
    ----------
    payload : dict
        The request payload containing:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    try:
        # Validate headers
        headers = payload.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # Validate body
        body = payload.get("body", {})
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        if not isinstance(user_id, int) or not isinstance(new_email, str):
            return False

        # Basic email format check
        if not EMAIL_REGEX.match(new_email):
            return False

        # Check that the user exists
        if user_id not in database:
            return False

        # Perform the update
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # Any unexpected error results in a failure response
        return False