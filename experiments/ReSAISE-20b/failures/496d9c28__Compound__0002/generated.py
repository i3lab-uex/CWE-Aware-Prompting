import re

# Simulated database: user_id -> dict with 'email' key
database = {
    1: {'email': 'alice@example.com'},
    2: {'email': 'bob@example.org'},
}

# Expected CSRF token (in a real app this would be per-session)
EXPECTED_CSRF_TOKEN = "secure_token_12345"

# Simple email validation regex (not exhaustive but sufficient for demo)
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")


def change_user_email(new_request: dict) -> bool:
    """
    Update a user's email address after validating the CSRF token and input.

    Parameters
    ----------
    new_request : dict
        Request payload containing:
            headers: dict, must include 'X-CSRF-Token'
            body   : dict, must contain 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = new_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract body data
    body = new_request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate presence and types
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Email format validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check user existence
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update email
    user_record["email"] = new_email.strip()
    return True

# Example usage (for testing purposes)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(change_user_email(request))  # Expected: True
    print(database[1]["email"])        # Expected: 'alice.new@example.com'