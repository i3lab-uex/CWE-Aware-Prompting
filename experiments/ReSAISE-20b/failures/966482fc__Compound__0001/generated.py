import re

# Mock database of users: {user_id: {"email": "..."}}
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def _is_valid_email(email: str) -> bool:
    """Return True if the email matches a simple RFC‑5322 pattern."""
    return bool(EMAIL_REGEX.match(email))

def modify_user_email(req: dict) -> bool:
    """
    Update a user's email address after performing CSRF and data validation.

    Parameters
    ----------
    req : dict
        The HTTP request represented as a dictionary with keys:
            - 'headers': dict of HTTP headers
            - 'body'   : dict containing 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully; False otherwise.
    """
    # 1. CSRF protection: ensure the request contains a valid token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract user ID and new email from the request body
    body = req.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"]
    except (KeyError, ValueError):
        # Missing or malformed data
        return False

    # 3. Validate the new email format
    if not _is_valid_email(new_email):
        return False

    # 4. Check that the user exists in the mock database
    if user_id not in database:
        return False

    # 5. Perform the update
    database[user_id]["email"] = new_email
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    success = modify_user_email(request)
    print("Update successful:", success)
    print("Updated record:", database[1])