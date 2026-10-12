import re

# Mock database and CSRF token for demonstration purposes
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Simple email validation regex
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}"
    r"[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$"
)


def change_user_email(request_data: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request. Expected keys:
            - "headers": dict containing request headers.
            - "body": dict containing user data, e.g. {"user_id": 1, "new_email": "..."}.

    Returns
    -------
    bool
        True if the email was successfully updated; False otherwise.
    """
    # 1. CSRF token validation
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract user ID and new email from body
    body = request_data.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"].strip()
    except (KeyError, ValueError, AttributeError):
        # Missing or malformed data
        return False

    # 3. Validate new email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Verify that the user exists in the database
    if user_id not in database:
        return False

    # 5. Update the email
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected failure during the update should be treated as a failure
        return False

    return True


# Example usage (for testing only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(change_user_email(request))  # Expected: True
    print(database[1]["email"])       # Expected: "alice.new@example.com"