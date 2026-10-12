import re

# Simulated database: user_id -> {'email': ...}
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}

# Predefined CSRF token
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def modify_user_email(req: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Parameters
    ----------
    req : dict
        Request payload containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict, must contain 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body data
    body = req.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # Ensure user_id is an integer and present
    if not isinstance(user_id, int):
        return False

    # Ensure new_email is a string and matches the regex
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 3. Update the mock database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 4. Perform the update
    user_record["email"] = new_email.strip()
    return True

# Example usage (for testing purposes)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "newalice@example.com"},
    }
    print(modify_user_email(request))  # Should output: True
    print(database[1]["email"])        # Should output: newalice@example.com