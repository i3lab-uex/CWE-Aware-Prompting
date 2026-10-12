import re
from typing import Dict

# Simulated database and CSRF token for demonstration purposes.
database: Dict[str, Dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_value"

# Regular expression for basic email validation.
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def change_user_email(new_request: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Parameters
    ----------
    new_request : dict
        The incoming request object. Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id": <str or int>,
                    "new_email": "<email>"
                }
            }

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = new_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch: potential CSRF or forged request.
        return False

    # 2. Extract body parameters
    body = new_request.get("body", {})
    user_id = str(body.get("user_id")).strip() if body.get("user_id") is not None else ""
    new_email = str(body.get("new_email")).strip() if body.get("new_email") else ""

    # 3. Validate presence of required fields
    if not user_id or not new_email:
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Ensure the user exists in the database
    if user_id not in database:
        return False

    # 6. Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error during update leads to failure.
        return False

    return True