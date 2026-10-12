import re

# Simulated database and CSRF token for demonstration purposes
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def change_user_email(new_request: dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    new_request : dict
        Dictionary representing an HTTP request. Expected keys:
            - "headers": dict, must contain "X-CSRF-Token".
            - "body": dict, must contain "user_id" (int) and
                      "new_email" (str).

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # Validate presence of required parts
    headers = new_request.get("headers")
    body = new_request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID and new email
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # Basic email format validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # Check that the user exists
    if user_id not in database:
        return False

    # Update the email address atomically
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error should not leak details
        return False

    return True