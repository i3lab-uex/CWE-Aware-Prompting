import re

# Simulated database and CSRF token (would normally be stored securely)
database = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@domain.org"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Simple regex for email validation (not exhaustive but sufficient for demo)
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def _is_valid_email(email: str) -> bool:
    """Return True if the email matches a basic pattern."""
    return bool(EMAIL_REGEX.match(email))


def update_user_email(request: dict) -> bool:
    """
    Update a user's email address.

    Parameters
    ----------
    request : dict
        Dictionary containing:
            - 'headers': dict with 'X-CSRF-Token' key.
            - 'body': dict with 'user_id' (int) and 'new_email' (str).

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or CSRF token is invalid.
    """
    # 1. Validate presence of headers and body
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary")

    headers = request.get("headers", {})
    body = request.get("body", {})

    # 2. CSRF protection
    token = headers.get("X-CSRF-Token")
    if token != EXPECTED_CSRF_TOKEN:
        # Do not reveal whether the token was missing or wrong
        return False

    # 3. Extract user_id and new_email
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, TypeError, ValueError):
        return False

    # 4. Validate email format
    if not _is_valid_email(new_email):
        return False

    # 5. Update the simulated database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Ensure we are only updating the email field
    user_record["email"] = new_email
    return True


# Example usage (would normally be part of a test suite or application code)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "new@example.com"},
    }
    print(update_user_email(req))  # Should output: True
    print(database[1]["email"])   # Should output: new@example.com