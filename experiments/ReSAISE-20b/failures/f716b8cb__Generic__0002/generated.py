import re
from typing import Dict

# Simulated database: {user_id: {"email": str, ...}}
database: Dict[int, dict] = {}

# The expected CSRF token for validation
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def modify_user_email_address(user_request: Dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    user_request : dict
        Incoming request object. Expected to contain:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict, must contain 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Raises
    ------
    None

    Notes
    -----
    - The function performs CSRF token validation.
    - It validates the new email format before updating.
    - If the user ID does not exist, or validation fails, it returns False.
    """
    # Validate presence of required keys
    if not isinstance(user_request, dict):
        return False

    headers = user_request.get("headers", {})
    body = user_request.get("body", {})

    # CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID and new email
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # Check if user exists in the database
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        return False

    # Update the email address
    user_record["email"] = new_email
    return True