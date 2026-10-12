import re

# Simulated database and CSRF token (would normally be stored securely)
database = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Simple email validation regex (not exhaustive but sufficient for demo purposes)
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    r'|^"([^\\"]|(\\.))*")@([A-Z0-9]+(-[A-Z0-9]+)*\.)+[A-Z]{2,}$',
    re.IGNORECASE,
)


def update_user_email(request: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input.

    Parameters
    ----------
    request : dict
        Expected keys:
            headers: dict, must contain 'X-CSRF-Token'
            body: dict, must contain 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body parameters
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Update the database entry
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Perform the update
    try:
        user_record["email"] = new_email
        return True
    except Exception:
        # In a real scenario, log the exception
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "new@example.com"},
    }
    print(update_user_email(req))  # Should output: True
    print(database[1]["email"])   # Should output: new@example.com