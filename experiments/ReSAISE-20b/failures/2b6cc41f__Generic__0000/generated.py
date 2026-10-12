import re

# Mock database and CSRF token used by the application
database = {
    # Example: user_id -> {'email': 'old@example.com', ...}
    1: {'email': 'alice@example.com'},
    2: {'email': 'bob@example.org'}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")


def modify_user_email(req_data: dict) -> bool:
    """
    Update a user's email address.

    Parameters
    ----------
    req_data : dict
        HTTP request representation containing:
          - headers: mapping of header names to values.
          - body: mapping with keys 'user_id' and 'new_email'.

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF protection
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract user_id and new_email from body
    body = req_data.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"]
    except (KeyError, TypeError, ValueError):
        # Missing or malformed data
        return False

    # 3. Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check if user exists in the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the email
    user_record["email"] = new_email
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"}
    }
    result = modify_user_email(request)
    print("Update successful:", result)
    print("Updated database entry:", database[1])