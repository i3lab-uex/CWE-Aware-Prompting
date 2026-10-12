import re

# Mock database and CSRF token (normally these would be managed elsewhere)
database = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@domain.com"}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}$"
)


def _is_valid_email(email: str) -> bool:
    """Return True if email matches a basic RFC‑5322 pattern."""
    return bool(EMAIL_REGEX.match(email))


def modify_user_email(req_data: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_data : dict
        Dictionary containing HTTP request headers and body. Expected keys:
            - 'headers': dict with header names as keys
            - 'body'   : dict containing at least 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = req_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic input validation
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    if not _is_valid_email(new_email):
        return False

    # 4. Check that the user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the email
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # In a real scenario we would log the exception.
        return False


# Example usage (for demonstration only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "newaddress@example.com"}
    }
    result = modify_user_email(request)
    print("Update successful:", result)
    print("Database state:", database)