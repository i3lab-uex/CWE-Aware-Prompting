import re

# Simulated database of users (user_id -> user data)
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def _is_valid_email(email: str) -> bool:
    """
    Very simple email validation.
    """
    pattern = r"^[^@]+@[^@]+\.[^@]+$"
    return re.match(pattern, email) is not None

def change_user_email(new_request: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Parameters
    ----------
    new_request : dict
        Incoming request object containing:
            - headers: dict, should include 'X-CSRF-Token'
            - body: dict, must contain 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # Validate CSRF token
    headers = new_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Validate body presence
    body = new_request.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # Validate types
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # Validate email format
    if not _is_valid_email(new_email):
        return False

    # Retrieve user record
    user = database.get(user_id)
    if not user:
        return False

    # Update email
    user["email"] = new_email
    return True