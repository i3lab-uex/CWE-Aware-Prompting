import re
from typing import Dict

# Simulated database and CSRF token for the example.
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_value"

# Regular expression for a simple email validation.
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def _is_valid_email(email: str) -> bool:
    """
    Validate the email address using a regular expression.
    This is not exhaustive but catches common formatting errors.
    """
    return bool(EMAIL_REGEX.match(email))


def modify_user_email_address(user_request: Dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    user_request : dict
        The incoming request object containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body   : dict, must include 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or the CSRF token is invalid.
    """
    # 1. CSRF protection
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token mismatch – reject the request
        return False

    # 2. Extract body data
    body = user_request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic validation
    if user_id is None or new_email is None:
        return False

    # Ensure user_id is an integer
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return False

    # Validate email format
    if not _is_valid_email(new_email):
        return False

    # 4. Update the simulated database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["email"] = new_email
    return True


# Example usage (for demonstration; remove or comment out in production)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    success = modify_user_email_address(request)
    print("Update successful:", success)
    print("Updated record:", database[1])