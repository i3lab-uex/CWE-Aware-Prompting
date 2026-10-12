import re

# Mock database: user_id -> { "email": str, ... }
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}

# Expected CSRF token that must be present in request headers
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Simple email regex (RFC 5322 compliant regex is very long, this suffices for demo)
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$")


def change_user_email(request_data: dict) -> bool:
    """
    Update the email address of a user.

    Parameters
    ----------
    request_data : dict
        Dictionary containing HTTP request data. Expected keys:
            - "headers": dict of request headers.
            - "body": dict containing user data. Expected keys:
                * "user_id": int
                * "new_email": str

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.

    Raises
    ------
    ValueError
        If required data is missing or malformed.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Reject request due to missing or incorrect CSRF token
        return False

    # 2. Extract body data
    body = request_data.get("body", {})
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that user exists in the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the email
    try:
        user_record["email"] = new_email
    except Exception:
        # Any unexpected error should not expose internal details
        return False

    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Successful update
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(change_user_email(request))  # True

    # CSRF failure
    bad_request = {
        "headers": {"X-CSRF-Token": "bad-token"},
        "body": {"user_id": 1, "new_email": "alice.bad@example.com"},
    }
    print(change_user_email(bad_request))  # False