import re

# Mock database and CSRF token (would normally be stored securely)
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"}
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_value"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z0-9]{2,}$")


def edit_user_email(req_payload: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_payload : dict
        Dictionary representing an HTTP request. Expected keys:
            - "headers": dict containing request headers (including CSRF token)
            - "body": dict containing:
                * "user_id" : int
                * "new_email" : str

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or the CSRF token is invalid.
    """
    # Validate request structure
    if not isinstance(req_payload, dict):
        raise ValueError("Invalid request payload format")

    headers = req_payload.get("headers", {})
    body = req_payload.get("body", {})

    # CSRF protection
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Reject request due to missing/invalid CSRF token
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

    # Ensure user exists in the database
    if user_id not in database:
        return False

    # Update email
    try:
        database[user_id]["email"] = new_email
    except Exception:
        return False

    return True