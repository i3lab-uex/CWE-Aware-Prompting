import re

# Simulated database and CSRF token for demonstration purposes.
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Regular expression for a simple email validation.
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def change_user_email(new_request: dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    new_request : dict
        Incoming request containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict, must contain 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = new_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user_id and new_email from body
    body = new_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"].strip()
    except (KeyError, ValueError, AttributeError):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Verify user exists in database
    if user_id not in database:
        return False

    # 5. Update the email address
    database[user_id]["email"] = new_email
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": "secure-token-123"},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(change_user_email(request))  # Should output: True
    print(database[1]["email"])        # Should output: alice.new@example.com