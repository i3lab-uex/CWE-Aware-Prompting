import re
from typing import Dict, Any

# Simulated database and CSRF token
database: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Regular expression for a simple but reasonable email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def modify_user_email_address(user_request: Dict[str, Any]) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    user_request : dict
        Incoming request containing 'headers' and 'body'.
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id": <int>,
                    "new_email": "<email>"
                }
            }

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    try:
        # 1. CSRF token validation
        headers = user_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract body parameters
        body = user_request.get("body", {})
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        # 3. Basic type and presence checks
        if not isinstance(user_id, int) or not isinstance(new_email, str):
            return False

        # 4. Email format validation
        if not EMAIL_REGEX.match(new_email):
            return False

        # 5. Check that user exists
        if user_id not in database:
            return False

        # 6. Update the email
        database[user_id]["email"] = new_email.strip()
        return True

    except Exception:
        # Any unexpected error results in a failed update
        return False